# -*- coding: utf8 -*-

from . import backtick_
import re
import os

__all__ = ('Fdisk',)


class Fdisk(backtick_.BackTick):

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
            # Partition header
            r'^(?P<header>(Device)\s+(Start)\s+(End)' +
            r'(?:\s+(Sectors))?\s+(Size)\s+(Type))\s*$',
            # Partition row (must be last)
            r'^(?P<row>(\/\S+)(?:\s+(\S+))*)$'
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

    @classmethod
    def command(cls, **kw):
        return kw.get('fdisk', 'fdisk')

    @classmethod
    def flags(cls, flags, **kw):
        return ['-l'] + flags

    @classmethod
    def parse(cls, output):
        content = []
        for paragraph in re.split(r'\n\n\n+', output):
            cls._parse_paragraph(content, paragraph)
        return content

    @classmethod
    def kwargs(self, **kw):
        kwargs = super().kwargs(**kw)
        if 'env' not in kwargs:
            kwargs['env'] = os.environ
        kwargs['env']['LC_NUMERIC'] = 'C'  # fixes decimal point to be '.'
        return kwargs

    @classmethod
    def _parse_paragraph(cls, content, paragraph):
        disk = dict()
        for line in paragraph.splitlines():
            cls._parse_line(disk, line)
        content.append(disk)

    @classmethod
    def _parse_line(cls, disk, line):
        for expr in cls._expressions:
            match = re.match(expr, line)
            if match:
                cls._store_info(disk, match)
                return True
        # FIXME: issue some warning here
        return False

    @classmethod
    def _store_info(cls, disk, match):
        groupdict = match.groupdict()
        if 'header' in groupdict:
            cls._store_table_header(disk, match)
        elif 'row' in groupdict:
            cls._store_table_row(disk, groupdict)
        elif 'empty' not in groupdict:
            cls._store_disk_info(disk, groupdict)

    @classmethod
    def _store_table_header(cls, disk, match):
        cols = match.groups()[1:]
        disk['header'] = [c.lower() for c in cols if c is not None]

    @classmethod
    def _store_table_row(cls, disk, groupdict):
        if 'partitions' not in disk:
            disk['partitions'] = []
        header = disk['header']
        row = groupdict['row'].split(maxsplit=len(header)-1)
        pairs = zip(header, row)
        disk['partitions'].append({k: cls._convert(k, v) for k, v in pairs})

    @classmethod
    def _store_disk_info(cls, disk, groupdict):
        disk.update({k: cls._convert(k, v) for k, v in groupdict.items()})

    @classmethod
    def _convert(cls, key, val):
        conv = cls._converters.get(key, lambda x: x)
        return conv(val)


# vim: set ft=python et ts=4 sw=4:
