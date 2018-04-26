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
        kwargs = dict({tool: self.getarg(tool, tool)}, **(kw or {}))
        return klass.new(*args, **kwargs)

    def _fdisk_probe(self, devices=None):
        return self._probe(FdiskProbe, 'fdisk', (devices,))

    def _sfdisk_probe(self, device):
        return self._probe(SfdiskProbe, 'sfdisk', (device,))

    def _lsblk_probe(self, devices=None):
        return self._probe(LsBlkProbe, 'lsblk', (devices,))

    @classmethod
    def _backup_cmd_stdout(cls, ctx, cmd, arcfile):
        out = subprocess.check_output(cmd, universal_newlines=True)
        ctx.archive.writestr(arcfile, out)

    @classmethod
    def _backup_cmd_outfile(cls, ctx, cmd, arcfile, outfile):
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL)
        ctx.archive.write(outfile, arcfile)

    def _register_file(self, ctx, name, **kw):
        ctx.archive.metadata.files[name] = dict({'name': name}, **kw)

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
        meta = ArchiveMetadata(self._newgraph())
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
        graph = ctx.archive.metadata.graph
        for node in graph.nodes:
            partab = graph.node(node).partition_table
            if partab:
                self._backup_partition_table(ctx, partab)

    def _do_backup(self, ctx):
        # Start backup
        self._backup_partition_tables(ctx)
        return 0

    def run(self):
        with self._newcontext() as ctx:
            return self._do_backup(ctx)
        return 0


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4: