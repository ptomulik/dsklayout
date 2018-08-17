# -*- coding: utf8 -*-
"""Provides the VgCfgBackupExt class
"""

from . import ext_

__all__ = ('VgCfgBackupExt',)


class VgCfgBackupExt(ext_.CliExt):

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
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
