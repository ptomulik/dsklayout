# -*- coding: utf8 -*-
"""`dsklayout.device.device_`

Provides the Device class
"""

from ..util import dispatch
from .. import model

import abc

__all__ = ('Device',)


class Device(object, metaclass=abc.ABCMeta):
    """Represents a block device"""

    __slots__ = ()

    @classmethod
    @dispatch.on(1)
    def new(cls, spec):
        raise TypeError("%s is not supported by %s" % (type(spec), __qualname__))

    @classmethod
    @dispatch.when(model.BlkDev)
    def new(cls, blkdev):
        return cls.newFromBlkDev(blkdev)

    @classmethod
    def newFromBlkDev(cls, blkdev):
        pass

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
