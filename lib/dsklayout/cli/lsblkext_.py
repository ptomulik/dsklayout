# -*- coding: utf8 -*-
"""Provides the LsBlkExt class
"""

from . import cmdext_
from ..probe import LsBlk

__all__ = ('LsBlkExt',)


class LsBlkExt(cmdext_.CmdExt):

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

    def new(self):
        kwargs = {'lsblk': self.arguments.lsblk}
        return LsBlk.new(self.arguments.devices, **kwargs)

    def graph(self):
        return self.new().graph()


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
