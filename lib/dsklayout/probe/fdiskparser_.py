# -*- coding: utf8 -*-

import re

__all__ = ('FdiskParser', )


class FdiskParser:
    """Parser for :class:`FdiskProbe`.

    The class implements a parser for :manpage:`fdisk(8)` reports, like the
    following

    .. code-block:: console

        Disk /dev/sda: 931,5 GiB, 1000204886016 bytes, 1953525168 sectors
        Units: sectors of 1 * 512 = 512 bytes
        Sector size (logical/physical): 512 bytes / 512 bytes
        I/O size (minimum/optimal): 512 bytes / 512 bytes
        Disklabel type: gpt
        Disk identifier: 57529E7C-2B3F-41F8-B974-74A93F1127F1

        Device       Start        End    Sectors  Size Type
        /dev/sda1     2048       4095       2048    1M BIOS boot
        /dev/sda2     4096    2101247    2097152    1G Linux RAID
        /dev/sda3  2101248 1889538047 1887436800  900G Linux RAID


        Disk /dev/sdb: 931,5 GiB, 1000204886016 bytes, 1953525168 sectors
        Units: sectors of 1 * 512 = 512 bytes
        Sector size (logical/physical): 512 bytes / 512 bytes
        I/O size (minimum/optimal): 512 bytes / 512 bytes
        Disklabel type: gpt
        Disk identifier: 57529E7C-2B3F-41F8-B974-74A93F1127F1

        Device       Start        End    Sectors  Size Type
        /dev/sdb1     2048       4095       2048    1M BIOS boot
        /dev/sdb2     4096    2101247    2097152    1G Linux RAID
        /dev/sdb3  2101248 1889538047 1887436800  900G Linux RAID
    """

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

    def parse(self, text):
        """Parse :manpage:`fdisk(8)` report.

        :param str text:
            the text to be parsed.
        :return:
            a list of entries, one for each disk; the returned list is
            later used as :attr:`FdiskProbe.content`.
        :rtype: list

        The function is prepared to parse "multi-paragraph" reports generated
        by :manpage:`fdisk(8)` (one paragraph per disk device). For each
        paragraph, a dict entry is added to the list being returned. An entry
        is simply a dictionary, representing fields extracted from the report
        (field names are converted to lower case).
        """
        content = []
        for paragraph in re.split(r'\n\n\n+', text):
            self._parse_paragraph(content, paragraph)
        return content

    @staticmethod
    def _parse_paragraph(content, paragraph):
        disk = dict()
        table = {'header': None, 'rows': []}
        for line in paragraph.splitlines():
            FdiskParser._parse_line(disk, table, line)
        if table['header'] and table['rows']:
            FdiskParser._postprocess_table(disk, table)
        content.append(disk)

    @staticmethod
    def _parse_line(disk, table, line):
        for expr in FdiskParser._expressions:
            match = re.match(expr, line)
            if match:
                FdiskParser._store_parsed_line(disk, table, match)
                return True
        # FIXME: issue some warning here
        return False

    @staticmethod
    def _store_parsed_line(disk, table, match):
        groups = match.groupdict()
        if 'header' in groups:
            table['header'] = groups['header']
        elif 'row' in groups:
            table['rows'].append(groups['row'])
        elif 'empty' not in groups:
            FdiskParser._store_disk_info(disk, groups)

    @staticmethod
    def _store_disk_info(disk, groups):
        disk.update({k: FdiskParser._convert(k, v) for k, v in groups.items()})

    @staticmethod
    def _convert(key, val):
        conv = FdiskParser._converters.get(key, lambda x: x)
        return conv(val)

    @staticmethod
    def _postprocess_table(disk, table):
        header = table['header']
        rows = table['rows']
        pattern = FdiskParser._build_row_pattern(header, rows)
        ranges = FdiskParser._determine_columns(header, pattern)
        disk['partitions'] = []
        keys = [k.lower() for k in header.split()]
        for row in rows:
            entry = {k: FdiskParser._convert(k, row[slice(*ranges[k])].strip())
                     for k in keys}
            disk['partitions'].append(entry)

    @staticmethod
    def _build_row_pattern(header, rows):
        lines = [header] + rows
        maxlen = max([len(x) for x in lines])
        pattern = maxlen * [' ']
        for line in lines:
            FdiskParser._update_row_pattern(pattern, line)
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
        nongreedy = [c for c in cols if c.lower() not in FdiskParser._greedy]
        greedy = [c for c in cols if c.lower() in FdiskParser._greedy]
        for col in nongreedy:
            key = col.lower()
            rng[key] = FdiskParser._determine_column(header, col, pattern)
        for col in greedy:
            key = col.lower()
            rng[key] = FdiskParser._determine_column(header, col, pattern, rng)
        return rng

    @staticmethod
    def _determine_column(header, col, pattern, rng=None):
        left = header.index(col)
        right = left + len(col)
        key = col.lower()
        align = FdiskParser._alignment.get(key, '?')
        if align == 'l':
            right = FdiskParser._adjust_right(pattern, left, right, rng)
        elif align == 'r':
            left = FdiskParser._adjust_left(pattern, left, right, rng)
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
