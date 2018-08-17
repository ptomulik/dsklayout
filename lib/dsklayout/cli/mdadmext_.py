# -*- coding: utf8 -*-
"""Provides the MdadmExt class
"""

from . import ext_

__all__ = ('MdadmExt',)


class MdadmExt(ext_.CliExt):

    __slots__ = ()

    @property
    def name(self):
        return 'mdadm'

    def add_arguments(self, parser):
        parser.add_argument('--mdadm',
                            dest='mdadm',
                            metavar="PROG",
                            default='mdadm',
                            help="name or path to mdadm program")


# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
