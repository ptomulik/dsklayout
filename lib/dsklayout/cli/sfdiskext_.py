# -*- coding: utf8 -*-
"""Provides the SfdiskExt class
"""

from . import cmdext_
from ..probe import SfdiskProbe

__all__ = ('SfdiskExt',)


class SfdiskExt(cmdext_.CmdExt):

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

    def probe(self, device):
        kwargs = {'sfdisk': self.arguments.sfdisk}
        return SfdiskProbe.new(device, **kwargs)

    def backup(self, device, outfile):
        cmd = [self.arguments.sfdisk, '--dump', device]
        with open(outfile, 'w') as f:
            f.write(subprocess.check_output(cmd))

    def restore(self, device, infile):
        cmd = [self.arguments.sfdisk, device]
        with open(infile, 'r') as f:
            subprocess.check_call(cmd, stdin=f)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
