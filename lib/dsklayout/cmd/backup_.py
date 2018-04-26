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


class BackupCmd(cmd_.Cmd):

    __slots__ = ()

    def _tmpdir(self):
        """Create temporary directory"""
        kwargs = {'dir': self.getargument('tmpdir'),
                  'prefix': self.getargument('tmpdir_prefix')}
        return tempfile.TemporaryDirectory(**kwargs)

    def _fdisk_probe(self, devices=None):
        kwargs = {'fdisk': self.getargument('fdisk','fdisk')}
        return FdiskProbe.new(devices, **kwargs)

    def _sfdisk_probe(self, device):
        kwargs = {'sfdisk': self.getargument('sfdisk', 'sfdisk')}
        return SfdiskProbe.new(device, **kwargs)

    def _sfdisk_backup(self, device, outfile):
        cmd = [self.getargument('sfdisk', 'sfdisk'), '--dump', device]
        with open(outfile, 'w') as f:
            f.write(subprocess.check_output(cmd, universal_newlines=True))

    def _lsblk_probe(self, devices=None):
        kwargs = {'lsblk': self.getargument('lsblk', 'lsblk')}
        return LsBlkProbe.new(devices, **kwargs)

    def _lsblk_graph(self, devices=None):
        return self._lsblk_probe(devices).graph()

    def _probe_partab(self, dev):
        # FIXME: catch errors... return None on soft errors...
        return self._sfdisk_probe(dev).partab(dev)

    def _inject_partition_tables(self, graph):
        search = Dfs(direction='outward')
        injector = ParTabIn(self._probe_partab)
        search(graph, graph.roots(), **injector.callbacks)

    def _tmpdir_file(self, tmpdir, name):
        return os.path.join(tmpdir, os.path.basename(name))

    def _backed_file(self, tmpdir, name):
        return os.path.join(os.path.basename(name))

    def _backup_partition_table_gpt(self, tmpdir, partab, recovery):
        outfile = self._tmpdir_file(tmpdir, partab.device + '.sgdisk')
        self.sgdisk.backup(partab.device, outfile)
        infile = self._backed_file(tmpdir, partab.device + '.sgdisk')
##        cmd = self.sgdisk.restorecmd(partab.device, infile)
##        recovery.append(' '.join(cmd))

    def _backup_partition_table_dos(self, tmpdir, partab, recovery):
        outfile = self._tmpdir_file(tmpdir, partab.device + '.sfdisk')
        self._sfdisk_backup(partab.device, outfile)
        infile = self._backed_file(tmpdir, partab.device + '.sfdisk')
##        cmd = self.sfdisk.restorecmd(partab.device, infile)
##        recovery.append(' '.join(cmd))

    def _backup_partition_table(self, tmpdir, partab, recovery):
        label = partab.label
        try:
            backup = getattr(self, '_backup_partition_table_%s' % label)
        except AttributeError:
            raise RuntimeError("unsupported disk label %s" % repr(label))
        else:
            return backup(tmpdir, partab, recovery)

    def _backup_partition_tables(self, tmpdir, graph, recovery):
        for node in graph.nodes:
            partab = graph.node(node).partition_table
            if partab:
                self._backup_partition_table(tmpdir, partab, recovery)

    def _write_recovery_script(self, tmpdir, name, commands):
        outfile = self._tmpdir_file(tmpdir, name)
        with open(outfile, 'w') as f:
            f.write('#!/bin/sh\n')
            for cmd in commands:
                f.write("%s\n" % cmd)

    def _pack_tmpdir(self, tmpdir, outfile):
        with tarfile.open(outfile) as tar:
            tar.add(tmpdir, os.path.basename(tmpdir))

    def _do_backup(self, archive, tmpdir):
        graph = self._lsblk_graph(self.getargument('devices'))
        self._inject_partition_tables(graph)
        # Start backup
        recovery = []
        self._backup_partition_tables(tmpdir, graph, recovery)
        self._write_recovery_script(tmpdir, 'recover.sh', recovery)
        # archivize contents of tmpdir into a tar archive...
        self._pack_tmpdir(tmpdir, self.getargument('outfile'))

    def run(self):
        with self._tmpdir() as tmpdir, \
             Archive.new(self.argument('outfile'), 'w') as archive:
            return self._do_backup(archive, tmpdir)
        return 0


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
