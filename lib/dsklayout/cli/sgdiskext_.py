# -*- coding: utf8 -*-
"""Provides the SgdiskExt class
"""

from . import ext_

__all__ = ('SgdiskExt',)


class SgdiskExt(ext_.CliExt):

    __slots__ = ()

    @property
    def name(self):
        return 'sgdisk'

    def add_arguments(self, parser):
        parser.add_argument('--sgdisk',
                            dest='sgdisk',
                            metavar="PROG",
                            default='sgdisk',
                            help="name or path to sgdisk program")


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
