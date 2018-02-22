# -*- coding: utf8 -*-
"""`dsklayout.device.device_`

Provides the Device class
"""

from .. import util

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


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
