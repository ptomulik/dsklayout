# -*- coding: utf8 -*-
"""Provides the CliBackupCmd class
"""

from . import cmd_
from . import fdiskext_
from . import lsblkext_
from . import mdadmext_
from . import sfdiskext_
from . import sgdiskext_
from . import tmpdirext_
from . import vgcfgbackupext_

from ..cmd import *

__all__ = ('CliBackupCmd',)


class CliBackupCmd(cmd_.CliCmd):

    __slots__ = ()

    def __init__(self):
        super().__init__()
        self.add_extension(lsblkext_.LsBlkExt())
        self.add_extension(fdiskext_.FdiskExt())
        self.add_extension(sfdiskext_.SfdiskExt())
        self.add_extension(sgdiskext_.SgdiskExt())
        self.add_extension(mdadmext_.MdadmExt())
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

    def run(self):
        return BackupCmd(vars(self.arguments)).run()


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
