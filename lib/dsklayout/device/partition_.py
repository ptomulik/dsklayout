# -*- coding: utf8 -*-
"""Provides the Partition class
"""

from .. import util

__all__ = ('Partition',)


class Partition(util.FactorySubject):
    """Represents a single entry of PartitionTable"""

    __slots__ = ('properties_',)

    _property_map = {
        'device': 'device',
        'units': 'units',
        'start': 'start',
        'end': 'end',
        'size': 'size',
        'type': 'type',
        'type_name': 'type-name'
    }

    def __init__(self, properties=None):
        self._properties = properties if partitions is not None else dict()


util.add_dict_getters(Partition, Partition._property_map, '_properties')

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
