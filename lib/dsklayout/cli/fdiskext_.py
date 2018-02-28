# -*- coding: utf8 -*-
"""Provides the FdiskExt class
"""

from . import cmdext_
from ..probe import FdiskProbe

__all__ = ('FdiskExt',)


class FdiskExt(cmdext_.CmdExt):

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

    def probe(self, devices=None):
        kwargs = {'fdisk': self.arguments.fdisk}
        return FdiskProbe.new(devices, **kwargs)


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
