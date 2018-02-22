# -*- coding: utf8 -*-
"""`dsklayout.device.disk_`

Provides the Disk class
"""

from . import device_
from .. import model
from .. import util

__all__ = ('Disk',)


class Disk(device_.Device):
    """Represents a disk device"""

    __slots__ = ()

    @classmethod
    @util.dispatch.on('spec')
    def supports(cls, spec):
        return False

    @classmethod
    @util.dispatch.when(model.BlkDev)
    def supports(cls, spec):
        return spec.type == 'disk'


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
