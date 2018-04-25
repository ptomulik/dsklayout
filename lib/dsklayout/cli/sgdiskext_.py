# -*- coding: utf8 -*-
"""Provides the SgdiskExt class
"""

from . import ext_
##from ..probe import SgdiskProbe

import subprocess

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

##    def probe(self, device):
##        kwargs = {'sgdisk': self.arguments.sgdisk}
##        return SgdiskProbe.new(device, **kwargs)

    def backupcmd(self, device, outfile):
        return [self.arguments.sgdisk, '--backup', outfile, device]

    def restorecmd(self, device, infile):
        return [self.arguments.sgdisk, '--load-backup', infile, device]

    def backup(self, device, outfile):
        """Backup partition table to a file"""
        cmd = self.backupcmd(device, outfile)
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL)

    def restore(self, device, infile):
        cmd = self.restorecmd(device, infile)
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL)


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
