# -*- coding: utf8 -*-
"""Provides the BackupCmd class
"""

from . import cmd_
from . import lsblkext_

__all__ = ('BackupCmd',)


class BackupCmd(cmd_.Cmd):

    __slots__ = ()

    def __init__(self):
        super().__init__()
        self.add_extension(lsblkext_.LsBlkExt())

    @property
    def name(self):
        return 'backup'

    @property
    def properties(self):
        return {'description': 'backup disk layout'}

    def add_cmd_arguments(self, parser):
        parser.add_argument("devices", metavar='DEV', nargs='*',
                            help="block device to be included in backup")

    def run(self):
        return 0

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
