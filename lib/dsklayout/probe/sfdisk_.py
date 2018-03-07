# -*- coding: utf8 -*-

from . import backtick_
from .. import util
import json

__all__ = ('SfdiskProbe', 'SfdiskPartitionTable')


class SfdiskProbe(backtick_.BackTickProbe):


    _ptable_map = {
        'label': 'label',
        'id': 'id',
        'device': 'device',
        'unit': 'units',
    }

    _ptable_part_map = {
        'node': 'device',
        'start': 'start',
        'size': 'size',
        'uuid': 'uuid',
        'type': 'type',
        'name': 'name',
    }

    @property
    def entries(self):
        """Device names of all content entries"""
        return [self.content['partitiontable'].get('device')]

    @property
    def ptables(self):
        """Device names of content entries with a partition table"""
        return self.entries

    def entry(self, name):
        """Returns a single entry identified by device name"""
        entry = self.content['partitiontable']
        if name == entry.get('device'):
            return entry
        else:
            raise ValueError("invalid device name: %s" % repr(name))

    def ptable(self, name):
        entry = self.entry(name)
        ptable = {self._ptable_map.get(k, k): v for k, v in entry.items()
                  if k not in ('partitions', )}
        ptable['partitions'] = list(
            {self._ptable_part_map.get(k, k): v for k, v in p.items()}
            for p in entry['partitions']
        )
        for partition in ptable['partitions']:
            try:
                start = p['start']
                size = p['size']
            except KeyError:
                pass
            else:
                p['end'] = int(start) + int(size) - 1

        return ptable

    @classmethod
    def command(cls, **kw):
        return kw.get('sfdisk', 'sfdisk')

    @classmethod
    def flags(cls, flags, **kw):
        return ['-J'] + flags

    @classmethod
    def parse(cls, output):
        return json.loads(output)


class SfdiskPartitionTable(object):
    """A single partition table extracted from SfdiskProbe"""

    def __init__(self, properties):
        self._properties = properties

    @property
    def properties(self):
        return self._properties

    @classmethod
    @util.dispatch.on('src')
    def new(cls, src, *args, **kw):
        raise TypeError(("FdiskPartitionTable.new() can't accept %s as " +
                         "argument") % type(src).__name__)

    @classmethod
    @util.dispatch.when(SfdiskProbe)
    def new(cls, sfdisk, device):
        return cls(sfdisk.entry(device))


# vim: set ft=python et ts=4 sw=4:
