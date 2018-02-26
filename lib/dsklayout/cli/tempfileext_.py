# -*- coding: utf8 -*-
"""Provides the LsBlkExt class
"""

from . import cmdext_
from ..model import tempfile_

__all__ = ('LsBlkExt',)


class LsBlkExt(cmdext_.CmdExt):

    __slots__ = ()

    @property
    def name(self):
        return 'tempfile'

    def add_arguments(self, parser):
        parser.add_argument('--tempfile',
                            dest='tempfile',
                            metavar="PROG",
                            default='tempfile',
                            help="name or path to tempfile program")

    def new(self):
        kwargs = { 'tempfile': self.arguments.tempfile }
        return tempfile_.LsBlk.new(self.arguments.devices, **kwargs)

    def graph(self):
        return self.new().graph()


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
