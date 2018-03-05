# -*- coding: utf8 -*-
"""Provides the PartitionTable class
"""

from .. import util
from .. import probe

__all__ = ('PartitionTable',)


class PartitionTable(util.FactorySubject):
    """Represents a partition table"""

    __slots__ = ('properties_',)

    _property_map = {
        'disklabel': 'disklabel',
        'id': 'id',
    }

    def __init__(self, properties=None, partitions=None):
        self._properties = properties if partitions is not None else dict()
        self._partitions = partitions if partitions is not None else []

    @property
    def properties(self):
        return self._properties

    @property
    def partitions(self):
        return self._partitions

    @classmethod
    @util.dispatch.on('spec')
    def specargs(cls, spec):
        raise TypeError("PartitionTable.specargs() can't take %s as argument"
                        % type(spec).__name__)

    @classmethod
    @util.dispatch.when(probe.FdiskProbe)
    def specargs(cls, spec):
        pass

    @classmethod
    @util.dispatch.when(probe.SfdiskProbe)
    def specargs(cls, spec):
        pass

    @classmethod
    def supports(cls, spec):
        if isinstance(spec, (probe.FdiskProbe, probe.SfdiskProbe,)):
            return 1
        else:
            return False

    @classmethod
    def factory(cls):
        return util.Factory.of(cls, search=__package__)

    @classmethod
    def new(cls, spec):
        try:
            return cls.factory().produce(spec)
        except util.FactoryError:
            raise util.FactoryError("can't create PartitionTable from %s" %
                                    repr(spec))



util.add_dict_getters(PartitionTable, PartitionTable._property_map, '_properties')

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
