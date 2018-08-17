# -*- coding: utf8 -*-
"""Provides the TmpDirExt class
"""

from . import ext_

__all__ = ('TmpDirExt',)


class TmpDirExt(ext_.CliExt):

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


# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
