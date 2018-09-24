# -*- coding: utf8 -*-

from . import backtick_
from .. import util
import re
import os

__all__ = ('FdiskProbe', )


class FdiskProbe(backtick_.BackTickProbe):

    _colname = (r'(?:Device|Attrs|Boot|Bsize|Cpg|Cylinders|End|' +
                r'End-C/H/S|Flags|Fsize|Id|Name|Sectors|Size|Slice|Start|' +
                r'Start-C/H/S|Type|Type-UUID|UUID)')

    _expressions = [
            # Disk info
            r'^Disk\s+(?P<name>[^:]+):' +
            r'\s*(?P<size>\d+(?:\.\d+)?(?:\s*[a-zA-Z]{1,3})?)' +
            r',\s*(?P<bytes>\d+)\s+bytes,\s*(?P<sectors>\d+)\s+sectors$',
            # Geometry
            r'^Geometry:\s*(?P<heads>\d+)\s+heads,' +
            r'\s*(?P<tracksectors>\d+)\s+sectors/track,' +
            r'\s*(?P<cylinders>\d+)\s+cylinders$',
            # Units
            r'^Units:\s*(?P<units>(?:sectors|cylinders))\s+of' +
            r'(?:\s+\d+\s*\*\s*\d+\s*=)?\s*(?P<unitbytes>\d+)\s+bytes$',
            # Sector size
            r'^Sector\s+size\s+\(logical/physical\)\s*:' +
            r'\s*(?P<sector_log_size>\d+)\s+bytes\s*/' +
            r'\s*(?P<sector_phy_size>\d+)\s+bytes$',
            # I/O size
            r'^I/O\s+size\s+\(minimum/optimal\)\s*:' +
            r'\s*(?P<io_min_size>\d+)\s+bytes\s*/' +
            r'\s*(?P<io_opt_size>\d+)\s+bytes$',
            # Disklabel type
            r'^Disklabel\s+type\s*:\s*(?P<disklabel_type>\w+)$',
            # Disk identifier
            r'^Disk\s+identifier\s*:\s*(?P<disk_identifier>\S+)$',
            # Empty
            r'^(?P<empty>\s*)$',
            # Partition table header
            r'^(?P<header>' + _colname + r'(?:\s+' + _colname + r')*)$',
            # Partition table row (must be last)
            r'^(?P<row>(\/\S+)(?:\s+(\S+))*)$'
    ]

    _alignment = {
        'attrs': '?',
        'boot': '?',
        'bsize': 'r',
        'cpg': '?',
        'cylinders': 'r',
        'device': 'l',
        'end': 'r',
        'end-c/h/s': 'r',
        'flags': '?',
        'fsize': '?',
        'id': 'r',
        'name': 'l',
        'sectors': 'r',
        'size': 'r',
        'slice': 'l',
        'start': 'r',
        'start-c/h/s': 'r',
        'type': 'l',
        'type-uuid': 'l',
        'uuid': 'l',
    }

    _greedy = [
        'type',
        'name'
    ]

    _converters = {
        'bytes': int,
        'cylinders': int,
        'end': int,
        'heads': int,
        'io_min_size': int,
        'io_opt_size': int,
        'sector_log_size': int,
        'sector_phy_size': int,
        'sectors': int,
        'start': int,
        'tracksectors': int,
        'unitbytes': int,
    }

    _partab_map = {
      'disklabel_type': 'label',
      'disk_identifier': 'id',
      'name': 'device',
      'units': 'units',
      'bytes': 'bytes',
    }

    _partab_part_map = {
        'device': 'device',
        'start': 'start',
        'end': 'end',
        'sectors': 'size',
        'uuid': 'uuid',
        'type-uuid': 'type',
        'id': 'type',
        'name': 'name',
        'type': 'typename',
    }

    @property
    def entries(self):
        """Device names of all content entries."""
        return list(e.get('name') for e in self.content)

    @property
    def partabs(self):
        """Device names of entries having partition table."""
        return list(e.get('name') for e in self.content if 'partitions' in e)

    def entry(self, name):
        """Returns a single entry identified by device name."""
        try:
            return next((e for e in self.content if e.get('name') == name))
        except StopIteration:
            raise ValueError("invalid device name: %s" % repr(name))

    def partab(self, name):
        """Returns a dictionary which describes a partition table."""
        entry = self.entry(name)
        if 'partitions' not in entry:
            raise ValueError("entry %s has no partition table" % repr(name))
        partab = {self._partab_map.get(k, k): v for k, v in entry.items()
                  if k not in ('partitions', 'columns')}
        partab['partitions'] = list(
            {self._partab_part_map.get(k, k): v for k, v in p.items()}
            for p in entry['partitions']
        )
        return partab

    @classmethod
    def command(cls, **kw):
        return kw.get('fdisk', 'fdisk')

    @classmethod
    def flags(cls, flags, **kw):
        return ['-l', '--bytes'] + flags

    @classmethod
    def parse(cls, text):
        content = []
        for paragraph in re.split(r'\n\n\n+', text):
            cls._parse_paragraph(content, paragraph)
        return content

    @classmethod
    def kwargs(self, **kw):
        kwargs = super().kwargs(**kw)
        if 'env' not in kwargs:
            kwargs['env'] = os.environ
        kwargs['env']['LC_NUMERIC'] = 'C'  # fixes decimal point to be '.'
        return kwargs

    @staticmethod
    def _parse_paragraph(content, paragraph):
        disk = dict()
        for line in paragraph.splitlines():
            FdiskProbe._parse_line(disk, line)
        if 'table-header' in disk and 'table-rows' in disk:
            FdiskProbe._postprocess_table(disk)
            del disk['table-header']
            del disk['table-rows']
        content.append(disk)

    @staticmethod
    def _parse_line(disk, line):
        for expr in FdiskProbe._expressions:
            match = re.match(expr, line)
            if match:
                FdiskProbe._store_parsed_line(disk, match)
                return True
        # FIXME: issue some warning here
        return False

    @staticmethod
    def _store_parsed_line(disk, match):
        groups = match.groupdict()
        if 'header' in groups:
            FdiskProbe._store_table_header(disk, groups)
        elif 'row' in groups:
            FdiskProbe._store_table_row(disk, groups)
        elif 'empty' not in groups:
            FdiskProbe._store_disk_info(disk, groups)

    @staticmethod
    def _store_table_header(disk, groups):
        disk['table-header'] = groups['header']

    @staticmethod
    def _store_table_row(disk, groups):
        if 'table-rows' not in disk:
            disk['table-rows'] = []
        disk['table-rows'].append(groups['row'])

    @staticmethod
    def _store_disk_info(disk, groups):
        disk.update({k: FdiskProbe._convert(k, v) for k, v in groups.items()})

    @staticmethod
    def _convert(key, val):
        conv = FdiskProbe._converters.get(key, lambda x: x)
        return conv(val)

    @staticmethod
    def _postprocess_table(disk):
        header = disk['table-header']
        rows = disk['table-rows']
        pattern = FdiskProbe._build_row_pattern(header, rows)
        ranges = FdiskProbe._determine_columns(header, pattern)
        disk['partitions'] = []
        keys = [k.lower() for k in header.split()]
        disk['columns'] = header.split()
        for row in rows:
            entry = {k: FdiskProbe._convert(k, row[slice(*ranges[k])].strip())
                     for k in keys}
            disk['partitions'].append(entry)

    @staticmethod
    def _build_row_pattern(header, rows):
        lines = [header] + rows
        maxlen = max([len(x) for x in lines])
        pattern = maxlen * [' ']
        for line in lines:
            FdiskProbe._update_row_pattern(pattern, line)
        return ''.join(pattern)

    @staticmethod
    def _update_row_pattern(pattern, line):
        for i in range(0, len(line)):
            if not line[i].isspace():
                pattern[i] = '*'

    @staticmethod
    def _determine_columns(header, pattern):
        rng = dict()
        cols = header.split()
        nongreedy = [c for c in cols if c.lower() not in FdiskProbe._greedy]
        greedy = [c for c in cols if c.lower() in FdiskProbe._greedy]
        for col in nongreedy:
            key = col.lower()
            rng[key] = FdiskProbe._determine_column(header, col, pattern)
        for col in greedy:
            key = col.lower()
            rng[key] = FdiskProbe._determine_column(header, col, pattern, rng)
        return rng

    @staticmethod
    def _determine_column(header, col, pattern, rng=None):
        left = header.index(col)
        right = left + len(col)
        key = col.lower()
        align = FdiskProbe._alignment.get(key, '?')
        if align == 'l':
            right = FdiskProbe._adjust_right(pattern, left, right, rng)
        elif align == 'r':
            left = FdiskProbe._adjust_left(pattern, left, right, rng)
        return (left, right)

    @staticmethod
    def _adjust_left(pattern, left, right, rng):
        m = re.search(r'(?P<stars>\*+)$', pattern[:left])
        if m:
            left = min([left, left - len(m.group('stars'))])
        if rng is not None:
            maxleft = max([0] + [x[1]+1 for x in rng.values() if x[1] < left])
            left = min(maxleft, left)
        return left

    @staticmethod
    def _adjust_right(pattern, left, right, rng):
        m = re.match(r'(?P<stars>\*+)', pattern[left:])
        if m:
            right = max([right, left + len(m.group('stars'))])
        if rng is not None:
            l = [len(pattern)]
            minright = min(l + [x[0]-1 for x in rng.values() if x[0] > right])
            right = max([minright, right])
        return right


# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
