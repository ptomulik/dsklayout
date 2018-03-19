# -*- coding: utf8 -*-
"""Provides the PartitionTable class
"""

from . import partition_
from .. import util

__all__ = ('PartitionTable',)


class PartitionTable(object):
    """Represents a partition table"""

    __slots__ = ('_properties', '_partitions')

    _pp_map = {
        'label': 'label',
        'id': 'id',
        'device': 'device',
        'units': 'units',
    }

    def __init__(self, properties=None, partitions=None):
        self._properties = properties if properties is not None else dict()
        self._partitions = partitions if partitions is not None else []

    @property
    def properties(self):
        return self._properties

    @property
    def partitions(self):
        return self._partitions

    @classmethod
    def new(cls, partab):
        properties = {k: v for k,v in partab.items() if k in cls._pp_map}
        partitions = [partition_.Partition(p) for p in partab['partitions']]
        return cls(properties, partitions)



util.add_dict_getters(PartitionTable, PartitionTable._pp_map, '_properties')

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
