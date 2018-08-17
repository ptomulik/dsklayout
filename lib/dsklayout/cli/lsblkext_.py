# -*- coding: utf8 -*-
"""Provides the LsBlkExt class
"""

from . import ext_

__all__ = ('LsBlkExt',)


class LsBlkExt(ext_.CliExt):

    __slots__ = ()

    @property
    def name(self):
        return 'lsblk'

    def add_arguments(self, parser):
        parser.add_argument('--lsblk',
                            dest='lsblk',
                            metavar="PROG",
                            default='lsblk',
                            help="name or path to lsblk program")


# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
