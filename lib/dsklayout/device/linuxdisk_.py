# -*- coding: utf8 -*-
"""Provides the LinuxDisk class
"""

from . import linux_
from .. import model
from ..util import dispatch

__all__ = ('LinuxDisk',)


class LinuxDisk(linux_.LinuxDevice):
    """Represents a linux disk"""

    __slots__ = ()

    @classmethod
    @dispatch.on('spec')
    def supports(cls, spec):
        return False

    @classmethod
    @dispatch.when(model.LsBlkDev)
    def supports(cls, spec):
        return 2 if spec.type == 'disk' else 0


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
