# -*- coding: utf8 -*-
"""Provides the Device class
"""

from .. import util

__all__ = ('Device',)


class Device(util.FactorySubject):
    """Abstract base class for devices"""

    __slots__ = ()

    @classmethod
    def factory(cls):
        return util.Factory.of(cls, search=__package__)

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
