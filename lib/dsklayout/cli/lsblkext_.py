# -*- coding: utf8 -*-
"""Provides the LsBlkExt class
"""

from . import ext_
from ..probe import LsBlkProbe

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

    def probe(self, devices=None):
        kwargs = {'lsblk': self.arguments.lsblk}
        return LsBlkProbe.new(devices, **kwargs)

    def graph(self, devices=None):
        return self.probe(devices).graph()


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
