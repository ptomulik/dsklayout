# -*- coding: utf8 -*-
"""`dsklayout.device.device_`

Provides the Device class
"""

from ..util import dispatch
from .. import model

import abc
import sys
import inspect

__all__ = ('Device',)


class Device(object, metaclass=abc.ABCMeta):
    """Represents a block device"""

    __slots__ = ()

    @classmethod
    @abc.abstractmethod
    def type(cls):
        pass

    @classmethod
    @dispatch.on(1)
    def new(cls, spec):
        raise TypeError("%r is not supported by %s.new()" %
                        (type(spec).__name__, cls.__name__))

    @classmethod
    @dispatch.when(model.BlkDev)
    def new(cls, blkdev):
        return cls.new_from_blkdev(blkdev)

    @classmethod
    def new_from_blkdev(cls, blkdev):
        raise NotImplementedError("Not implemented yet")

    @staticmethod
    def subclasses():
        pred = lambda x : inspect.isclass(x) and \
                          issubclass(x, Device) and \
                          x is not Device
        return inspect.getmembers(sys.modules[__package__], pred)



# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
