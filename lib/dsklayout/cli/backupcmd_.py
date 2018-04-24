# -*- coding: utf8 -*-
"""Provides the BackupCmd class
"""

from . import cmd_
from . import lsblkext_
from . import fdiskext_
from . import sfdiskext_
from . import sgdiskext_
from . import vgcfgbackupext_
from . import tmpdirext_

from ..device import *
from ..graph import *
from ..visitor import *
from ..archive import *

import tarfile
import sys
import os

__all__ = ('BackupCmd',)


class BackupCmd(cmd_.Cmd):

    __slots__ = ()

    def __init__(self):
        super().__init__()
        self.add_extension(lsblkext_.LsBlkExt())
        self.add_extension(fdiskext_.FdiskExt())
        self.add_extension(sfdiskext_.SfdiskExt())
        self.add_extension(sgdiskext_.SgdiskExt())
        self.add_extension(vgcfgbackupext_.VgCfgBackupExt())
        self.add_extension(tmpdirext_.TmpDirExt())

    @property
    def name(self):
        return 'backup'

    @property
    def properties(self):
        return {'description': 'backup disk layout'}

    def add_cmd_arguments(self, parser):
        parser.add_argument("outfile", metavar='OUTFILE', help="output file")
        parser.add_argument("devices", metavar='DEV', nargs='*',
                            help="block device to be included in backup")

    def _probe_partab(self, dev):
        # FIXME: catch errors... return None on soft errors...
        return self.sfdisk.probe(dev).partab(dev)

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
        cmd = self.sgdisk.restorecmd(partab.device, infile)
        recovery.append(' '.join(cmd))

    def _backup_partition_table_mbr(self, tmpdir, partab, recovery):
        outfile = self._tmpdir_file(tmpdir, partab.device + '.sfdisk')
        self.sfdisk.backup(partab.device, outfile)
        infile = self._backed_file(tmpdir, partab.device + '.sfdisk')
        cmd = self.sfdisk.restorecmd(partab.device, infile)
        recovery.append(' '.join(cmd))

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
        taropts = {'format': tarfile.USTAR_FORMAT}
        with tarfile.open(outfile, 'w:gz', **taropts) as tar:
            tar.add(tmpdir, os.path.basename(tmpdir))

    def _do_backup(self, tmpdir):
        graph = self.lsblk.graph(self.arguments.devices)
        self._inject_partition_tables(graph)
        # Start backup
        recovery = []
        self._backup_partition_tables(tmpdir, graph, recovery)
        self._write_recovery_script(tmpdir, 'recover.sh', recovery)
        # archivize contents of tmpdir into a tar archive...
        self._pack_tmpdir(tmpdir, self.arguments.outfile)

    def run(self):
        with self.tmpdir.new() as tmpdir:
            return self._do_backup(tmpdir)
        return 0


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
