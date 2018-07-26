# -*- coding: utf8 -*-
"""Provides the BackupCmd class
"""

from . import cmd_

from ..archive import *
from ..cmd import *
from ..device import *
from ..graph import *
from ..probe import *
from ..visitor import *

import tempfile
import subprocess
import sys
import os


__all__ = ('BackupCmd',)

_mdadm_raid_types = ['raid0', 'raid1', 'raid4', 'raid5', 'raid6', 'raid10']

class _BackupContext:

    __slots__ = ('_tmpdir', '_archive')

    def __init__(self, tmpdir, archive):
        self._tmpdir = tmpdir
        self._archive = archive

    @property
    def tmpdir(self):
        return self._tmpdir.name

    @property
    def archive(self):
        return self._archive

    @property
    def lsblk_graph(self):
        return self.archive.metadata.lsblk_graph

    @property
    def lvm_probe(self):
        return self.archive.metadata.lvm_probe

    @property
    def files(self):
        return self.archive.metadata.files

    def __enter__(self):
        self._tmpdir.__enter__()
        self._archive.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        supp1 = self._archive.__exit__(exc_type, exc_val, exc_tb)
        supp2 = self._tmpdir.__exit__(exc_type, exc_val, exc_tb)
        return supp1 or supp2


class BackupCmd(cmd_.Cmd):

    __slots__ = ()

    def _mktmpdir(self):
        """Securely creates a temporary directory and returns a
        tempfile.TemporaryDirectory object which can be used as a context
        manager"""
        kwargs = self.mapargs({'dir': 'tmpdir',
                               'prefix': 'tmpdir_prefix',
                               'suffix': 'tmpdir_suffix'})
        return tempfile.TemporaryDirectory(**kwargs)

    def _probe(self, klass, tool, args, kw=None):
        if isinstance(tool, str):
            tools = {tool: self.getarg(tool, tool)}
        elif isinstance(tool, dict):
            tools = tool
        else:
            tools = {t: self.getarg(t,t) for t in tool}
        #kwargs = dict({tool: self.getarg(tool, tool)}, **(kw or {}))
        kwargs = dict(tools, **(kw or {}))
        return klass.new(*args, **kwargs)

    def _fdisk_probe(self, devices=None):
        return self._probe(FdiskProbe, 'fdisk', (devices,))

    def _sfdisk_probe(self, device):
        return self._probe(SfdiskProbe, 'sfdisk', (device,))

    def _lsblk_probe(self, devices=None):
        return self._probe(LsBlkProbe, 'lsblk', (devices,))

    def _lvm_probe(self, devices=None, **kw):
        return self._probe(LvmProbe, ('lvs', 'pvs', 'vgs'), (devices,), kw)

    @classmethod
    def _backup_cmd_stdout(cls, ctx, cmd, arcfile):
        out = subprocess.check_output(cmd, universal_newlines=True)
        ctx.archive.writestr(arcfile, out)

    @classmethod
    def _backup_cmd_outfile(cls, ctx, cmd, arcfile, outfile):
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL)
        ctx.archive.write(outfile, arcfile)

    def _register_file(self, ctx, name, **kw):
        ctx.files[name] = dict({'name': name}, **kw)

    def _sfdisk_backup(self, ctx, device, arcfile):
        cmd = [self.getarg('sfdisk', 'sfdisk'), '--dump', device]
        self._backup_cmd_stdout(ctx, cmd, arcfile)
        backupcmd = ' '.join([cmd[0], '--dump', device, '>', arcfile])
        restorecmd = ' '.join([cmd[0], device, '<', arcfile])
        self._register_file(ctx, arcfile,
                            type='sfdisk-backup',
                            device=device,
                            backupcmd=backupcmd,
                            restorecmd=restorecmd)

    def _sgdisk_backup(self, ctx, device, arcfile):
        outfile = os.path.join(ctx.tmpdir, arcfile)
        cmd = [self.getarg('sgdisk', 'sgdisk'), '--backup=%s' % outfile, device]
        self._backup_cmd_outfile(ctx, cmd, arcfile, outfile)
        backupcmd = ' '.join([cmd[0], '--backup=%s' % arcfile, device])
        restorecmd = ' '.join([cmd[0], '--load-backup=%s' % arcfile, device])
        self._register_file(ctx, arcfile,
                            type='sgdisk-backup',
                            device=device,
                            backupcmd=backupcmd,
                            restorecmd=restorecmd)

    def _lsblk_graph(self, devices=None):
        return self._lsblk_probe(devices).graph()

    def _newgraph(self):
        graph = self._lsblk_graph(self.getarg('devices'))
        self._inject_partition_tables(graph)
        return graph

    def _newcontext(self):
        tmpdir = self._mktmpdir()
        graph = self._newgraph()
        if [n for n in graph.nodes if graph.node(n).fstype == 'LVM2_member']:
            lvm_probe = self._lvm_probe(self.getarg('devices'))
        else:
            lvm_probe = None
        meta = ArchiveMetadata(lsblk_graph=graph, lvm_probe=lvm_probe)
        archive = Archive.new(self.arg('outfile'), 'w', metadata=meta)
        return _BackupContext(tmpdir, archive)

    def _probe_partab(self, dev):
        # FIXME: catch errors... return None on soft errors...
        return self._sfdisk_probe(dev).partab(dev)

    def _inject_partition_tables(self, graph):
        search = Dfs(direction='outward')
        injector = ParTabIn(self._probe_partab)
        search(graph, graph.roots(), **injector.callbacks)

    def _backup_partition_table_gpt(self, ctx, partab):
        arcfile = os.path.basename(partab.device) + '.sgdisk'
        self._sgdisk_backup(ctx, partab.device, arcfile)

    def _backup_partition_table_dos(self, ctx, partab):
        arcfile = os.path.basename(partab.device) + '.sfdisk'
        self._sfdisk_backup(ctx, partab.device, arcfile)

    def _backup_partition_table(self, ctx, partab):
        label = partab.label
        try:
            backup = getattr(self, '_backup_partition_table_%s' % label)
        except AttributeError:
            raise RuntimeError("unsupported disk label %s" % repr(label))
        else:
            return backup(ctx, partab)

    def _backup_partition_tables(self, ctx):
        graph = ctx.lsblk_graph
        for node in graph.nodes:
            partab = graph.node(node).partition_table
            if partab:
                self._backup_partition_table(ctx, partab)

    def _backup_mdraid_device(sefl, ctx, node):
        # mdadm --detail
        # TODO: add to metadata
        # TODO: save in an archive
        pass

    def _backup_mdraid_member(self, ctx, node):
        # mdadm --examine
        # TODO: add to metadata
        # TODO: save in an archive
        pass

    def _backup_node(self, ctx, graph, node, edge=None):
        partab = graph.node(node).partition_table
        if partab:
            self._backup_partition_table(ctx, partab)
        if graph.node(node).type in _mdadm_raid_types:
            self._backup_mdraid_device(ctx, graph.node)
        if graph.node(node).fstype == 'linux_raid_member':
            self._backup_mdraid_member(ctx, graph.node)

    def _backup_lvm(self, ctx):
        lvm = LvmProbe.new(lsblkgraph=ctx.lsblk_graph)

    def _backup(self, ctx):
        def ingress(graph, node, edge):
            return self._backup_node(ctx, graph, node, edge)
        search = Bfs(direction='inward', ingress_func=ingress)
        search(ctx.lsblk_graph, ctx.lsblk_graph.leafs())
        self._backup_lvm(ctx)
        return 0

    def run(self):
        with self._newcontext() as ctx:
            return self._backup(ctx)
        return 0


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
