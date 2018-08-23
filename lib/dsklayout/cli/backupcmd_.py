# -*- coding: utf8 -*-
"""Provides the CliBackupCmd class
"""

from . import cmd_
from . import progext_
from . import tmpdirext_

from ..cmd import *

__all__ = ('CliBackupCmd',)


class CliBackupCmd(cmd_.CliCmd):

    __slots__ = ()

    def __init__(self):
        super().__init__()
        progs = ('lsblk', 'fdisk', 'sfdisk', 'sgdisk', 'mdadm', 'vgcfgbackup',
                 'pvs', 'vgs', 'lvs')
        for prog in progs:
            self.add_extension(progext_.ProgExt(prog))
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

    def run(self):
        return BackupCmd(vars(self.arguments)).run()


# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
