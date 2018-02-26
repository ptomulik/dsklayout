# -*- coding: utf8 -*-
"""Provides the TmpDirExt class
"""

from . import cmdext_
import tempfile

__all__ = ('TmpDirExt',)


class TmpDirExt(cmdext_.CmdExt):

    __slots__ = ()

    @property
    def name(self):
        return 'tmpdir'

    def add_arguments(self, parser):
        parser.add_argument('--tmpdir',
                            dest='tmpdir',
                            metavar="DIR",
                            default=None,
                            help="where to create temporary directory")
        parser.add_argument('--tmpdir-prefix',
                            dest='tmpdir_prefix',
                            metavar='PFX',
                            default='dsklayout-',
                            help="prefix for temporary directory name")

    def new(self):
        kwargs = {'dir': self.arguments.tmpdir,
                  'prefix': self.arguments.tmpdir_prefix}
        return tempfile.TemporaryDirectory(**kwargs)


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
