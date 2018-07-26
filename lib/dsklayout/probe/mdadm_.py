# -*- coding: utf8 -*-

from . import backtick_

__all__ = ('MdadmProbe', )


class MdadmProbe(backtick_.BackTickProbe):

    @property
    def entries(self):
        """Device names of all devices covered"""
        return [self.content['partitiontable'].get('device')]

    @property
    def partabs(self):
        """Device names of devices having partition tables"""
        return self.entries

    def entry(self, name):
        """Returns a single entry identified by device name"""
        entry = self.content['partitiontable']
        if name == entry.get('device'):
            return entry
        else:
            raise ValueError("invalid device name: %s" % repr(name))

    def partab(self, name):
        """Returns a dictionary which describes a partition table."""
        entry = self.entry(name)
        partab = {self._partab_map.get(k, k): v for k, v in entry.items()
                  if k not in ('partitions', )}
        partab['partitions'] = list(
            {self._partab_part_map.get(k, k): v for k, v in p.items()}
            for p in entry['partitions']
        )
        for part in partab['partitions']:
            MdadmProbe._compute_partition_end(part)

        return partab

    @classmethod
    def command(cls, **kw):
        return kw.get('mdadm', 'mdadm')

    @classmethod
    def flags(cls, flags, **kw):
        return ['-J'] + flags

    @classmethod
    def parse(cls, output):
        return json.loads(output)

    @staticmethod
    def _compute_partition_end(part):
        try:
            start = part['start']
            size = part['size']
        except KeyError:
            pass
        else:
            part['end'] = int(start) + int(size) - 1


# vim: set ft=python et ts=4 sw=4:
