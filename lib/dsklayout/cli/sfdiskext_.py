# -*- coding: utf8 -*-
"""Provides the SfdiskExt class
"""

from . import ext_

__all__ = ('SfdiskExt',)


class SfdiskExt(ext_.CliExt):

    __slots__ = ()

    @property
    def name(self):
        return 'sfdisk'

    def add_arguments(self, parser):
        parser.add_argument('--sfdisk',
                            dest='sfdisk',
                            metavar="PROG",
                            default='sfdisk',
                            help="name or path to sfdisk program")


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
