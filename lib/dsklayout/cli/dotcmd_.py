# -*- coding: utf8 -*-
"""Provides the CliDotCmd class
"""

from . import cmd_
from . import lsblkext_

from ..cmd import *


__all__ = ('CliDotCmd',)


class CliDotCmd(cmd_.CliCmd):

    __slots__ = ()

    def __init__(self):
        super().__init__()
        self.add_extension(lsblkext_.LsBlkExt())

    @property
    def name(self):
        return 'dot'

    @property
    def properties(self):
        return {'description': 'generate graph representation of disk layout'}

    def add_cmd_arguments(self, parser):
        parser.add_argument("--view", action='store_true',
                            help="display graph instead of writting its source")
        parser.add_argument("-o", "--output", metavar='FILE',
                            help="write output to FILE instead of stdout")
        parser.add_argument("-i","--input", metavar='FILE',
                            help="use FILE as input instead of probing OS," +
                                 " FILE should be an archive previously" +
                                 " created with dsklayout backup")
        parser.add_argument("devices", metavar='DEV', nargs='*',
                            help="top-level block device to be included in graph")

    def run(self):
        return DotCmd(vars(self.arguments)).run()


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
