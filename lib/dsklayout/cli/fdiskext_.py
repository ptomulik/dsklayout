# -*- coding: utf8 -*-
"""Provides the FdiskExt class
"""

from . import ext_

__all__ = ('FdiskExt',)


class FdiskExt(ext_.CliExt):

    __slots__ = ()

    @property
    def name(self):
        return 'fdisk'

    def add_arguments(self, parser):
        parser.add_argument('--fdisk',
                            dest='fdisk',
                            metavar="PROG",
                            default='fdisk',
                            help="name or path to fdisk program")


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
