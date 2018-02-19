# -*- coding: utf8 -*-
"""`dsklayout.cli.lsblkext_`
"""

from . import cmdext_
from ..model import lsblk_

__all__ = ('LsBlkExt',)

class LsBlkExt(cmdext_.CmdExt):

    __slots__ = ()

    @property
    def name(self):
        return 'lsblk'

    def add_arguments(self, parser):
        parser.add_argument('--lsblk', dest='lsblk', metavar="PROG", default='lsblk',
                            help="name or path to lsblk program")

    def new(self):
        args = self.arguments
        return lsblk_.LsBlk.new(args.devices, lsblk=args.lsblk);

    def graph(self):
        return self.new().graph()



# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
