# -*- coding: utf8 -*-

from . import backtick_
from .. import util
import json

__all__ = ('SfdiskProbe', )


class SfdiskProbe(backtick_.BackTickProbe):

    _partab_map = {
        'label': 'label',
        'id': 'id',
        'device': 'device',
        'unit': 'units',
    }

    _partab_part_map = {
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
    def partabs(self):
        """Device names of content entries with a partition table"""
        return self.entries

    def entry(self, name):
        """Returns a single entry identified by device name"""
        entry = self.content['partitiontable']
        if name == entry.get('device'):
            return entry
        else:
            raise ValueError("invalid device name: %s" % repr(name))

    def partab(self, name):
        entry = self.entry(name)
        partab = {self._partab_map.get(k, k): v for k, v in entry.items()
                  if k not in ('partitions', )}
        partab['partitions'] = list(
            {self._partab_part_map.get(k, k): v for k, v in p.items()}
            for p in entry['partitions']
        )
        for part in partab['partitions']:
            try:
                start = part['start']
                size = part['size']
            except KeyError:
                pass
            else:
                part['end'] = int(start) + int(size) - 1

        return partab

    @classmethod
    def command(cls, **kw):
        return kw.get('sfdisk', 'sfdisk')

    @classmethod
    def flags(cls, flags, **kw):
        return ['-J'] + flags

    @classmethod
    def parse(cls, output):
        return json.loads(output)


# vim: set ft=python et ts=4 sw=4:
