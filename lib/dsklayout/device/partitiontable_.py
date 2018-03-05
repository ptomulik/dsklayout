# -*- coding: utf8 -*-
"""Provides the PartitionTable class
"""

from .. import util

__all__ = ('PartitionTable',)


class PartitionTable(object):
    """Represents a partition table"""

    __slots__ = ('properties_',)

##    @classmethod
##    def factory(cls):
##        return util.Factory.of(cls, search=__package__)
##
##    @classmethod
##    def new(cls, spec):
##        try:
##            return cls.factory().produce(spec)
##        except util.FactoryError:
##            raise util.FactoryError("can't create PartitionTable from %s" % repr(spec))


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
