# -*- coding: utf8 -*-
"""Provides the LinuxDevice class
"""

from . import device_
from .. import model
from .. import util


__all__ = ('LinuxDevice',)


class LinuxDevice(device_.Device):
    """Base class for Linux block devices"""

    __slots__ = ('_properties',)

    _pp_map = dict(model.LsBlkDev._pp_map, **{
        'partab': 'partab'
    })

    def __init__(self, properties):
        self._properties = properties

    @property
    def properties(self):
        return self._properties

    @classmethod
    @util.dispatch.on('spec')
    def specargs(cls, spec):
        raise TypeError("LinuxDevice.specargs() can't take %s as argument" %
                        type(spec).__name__)

    @classmethod
    @util.dispatch.when(model.LsBlkDev)
    def specargs(cls, spec):
        return (spec.properties,)

    @classmethod
    @util.dispatch.on('spec')
    def supports(cls, spec):
        return False

    @classmethod
    @util.dispatch.when(model.LsBlkDev)
    def supports(cls, spec):
        return 1


util.add_dict_getters(LinuxDevice, LinuxDevice._pp_map, '_properties')

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4: