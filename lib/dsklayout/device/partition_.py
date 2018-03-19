# -*- coding: utf8 -*-
"""Provides the Partition class
"""

from .. import util

__all__ = ('Partition',)


class Partition(object):
    """Represents a single entry of PartitionTable"""

    __slots__ = ('_properties',)

    _pp_map = {
        'device': 'device',
        'units': 'units',
        'start': 'start',
        'end': 'end',
        'size': 'size',
        'type': 'type',
        'type_name': 'type-name'
    }

    def __init__(self, properties=None):
        self._properties = properties if properties is not None else dict()

    @property
    def properties(self):
        return self._properties


util.add_dict_getters(Partition, Partition._pp_map, '_properties')

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
