# -*- coding: utf8 -*-
"""Provides the Device class
"""

from .. import model
from .. import util


__all__ = ('Device',)


class Device(object):
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


util.add_dict_getters(Device, Device._pp_map, '_properties')

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
