# -*- coding: utf8 -*-
"""`dsklayout.device.device_`

Provides the Device class
"""

from .. import util
from .. import model

import abc

__all__ = ('Device',)


class Device(util.FactorySubject):
    """Abstract base class for devices"""

    __slots__ = ()

    def __init__(self, properties):
        self._properties = properties

    @property
    def properties(self):
        return self._properties

    @classmethod
    def factory(cls):
        return util.Factory.factory(cls, search=__package__)

    @classmethod
    def new(cls, spec):
        try:
            return cls.factory().produce(spec)
        except util.FactoryError:
            raise util.FactoryError("can't create Device from %s" % repr(spec))

    @classmethod
    @util.dispatch.on('spec')
    def adjust(cls, spec):
        raise TypeError("Device.adjust() can't take %s as argument" % \
                         type(spec).__name__)

    @classmethod
    @util.dispatch.when(model.BlkDev)
    def adjust(cls, spec):
        return spec.properties


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
