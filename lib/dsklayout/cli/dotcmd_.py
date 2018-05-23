# -*- coding: utf8 -*-
"""Provides the CliDotCmd class
"""

from . import cmd_
from . import lsblkext_
from . import fdiskext_
from . import sfdiskext_
from . import sgdiskext_
from . import vgcfgbackupext_
from . import tmpdirext_

##from ..device import *
##from ..graph import *
##from ..visitor import *
##from ..archive import *
from ..cmd import *
##
##import tarfile
##import sys
##import os

__all__ = ('CliDotCmd',)


class CliDotCmd(cmd_.CliCmd):

    __slots__ = ()

    def __init__(self):
        super().__init__()
        self.add_extension(lsblkext_.LsBlkExt())
##        self.add_extension(fdiskext_.FdiskExt())
##        self.add_extension(sfdiskext_.SfdiskExt())
##        self.add_extension(sgdiskext_.SgdiskExt())
##        self.add_extension(vgcfgbackupext_.VgCfgBackupExt())
##        self.add_extension(tmpdirext_.TmpDirExt())

    @property
    def name(self):
        return 'dot'

    @property
    def properties(self):
        return {'description': 'generate graph representation of disk layout'}

    def add_cmd_arguments(self, parser):
        parser.add_argument("-i","--infile", metavar='INFILE',
                            help="use INFILE as input instead of probing OS," +
                                 " INFILE should be an archive previously" +
                                 " created with dsklayout backup")
        parser.add_argument("devices", metavar='DEV', nargs='*',
                            help="top-level block device to be included in graph")

    def run(self):
        return DotCmd(vars(self.arguments)).run()


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
