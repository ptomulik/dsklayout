# -*- coding: utf8 -*-
"""Provides the VgCfgBackupExt class
"""

from . import cmdext_
from ..probe import VgCfgBackupProbe

__all__ = ('VgCfgBackupExt',)


class VgCfgBackupExt(cmdext_.CmdExt):

    __slots__ = ()

    @property
    def name(self):
        return 'vgcfgbackup'

    def add_arguments(self, parser):
        parser.add_argument('--vgcfgbackup',
                            dest='vgcfgbackup',
                            metavar="PROG",
                            default='vgcfgbackup',
                            help="name or path to vgcfgbackup program")


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
