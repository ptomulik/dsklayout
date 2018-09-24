# -*- coding: utf8 -*-

from . import composite_
from . import backtick_
from . import lsblk_

from .. import util

import re

__all__ = ('MdadmDetailProbe', 'MdadmExamineProbe', 'MdadmProbe')


class _Convert:

    @classmethod
    def events(cls, val):
        m = re.match(r'(?P<hi>\d+)\.(?P<lo>\d+)', val)
        if m:
            return (int(m.group('hi')) << 32) | int(m.group('lo'))
        else:
            return int(val)

    @classmethod
    def ord(cls, val):
        return val if val == "this" else int(val)

    @classmethod
    def hex(cls, val):
        return int(val, 16)


class _MdadmBacktickProbe(backtick_.BackTickProbe):

    _converters = {
        'raid_devices': int,
        'total_devices': int,
        'preferred_minor': int,
        'active_devices': int,
        'working_devices': int,
        'failed_devices': int,
        'spare_devices': int,
        'events': _Convert.events,
        'ord': _Convert.ord,
        'number': int,
        'major': int,
        'minor': int,
        'raid_device': int,
        'feature_map': _Convert.hex,
    }

    @classmethod
    def convert(cls, key, val):
        try:
            convert = cls._converters[key]
        except KeyError:
            return val
        else:
            return convert(val)

    @classmethod
    def command(cls, **kw):
        return kw.get('mdadm', 'mdadm')

    @classmethod
    def parse(cls, output):
        return cls._parse(output)

    @classmethod
    def _match_device_name(cls, line):
        return re.match(r'^\s*(/+\w+(?:/+\w+)*):\s*$', line)

    @classmethod
    def _parse_device_name(cls, node, line):
        m = cls._match_device_name(line)
        if not m:
            return False
        node['device_name'] = m.group(1)
        return True

    @classmethod
    def _parse_keyval(cls, node, line):
        m = re.match(r'^\s*(\w+(?:\s+\w+)*)\s*:\s*(\S+(?:\s+\S+)*)\s*$', line)
        if not m:
            return False
        key = util.snake_case(m.group(1))
        node[key] = cls.convert(key, m.group(2))
        return True

    @classmethod
    def _parse_table_header(cls, node, line):
        m = re.match(r'^\s*(Number)\s+(Major)\s+(Minor)\s+(RaidDevice)' +
                     r'\s+(State)\s*$', line)
        if not m:
            return False
        node['table'] = {
            'headers': m.groups(),
            'colspan': [m.span(i) for i in range(1, 1+len(m.groups()))]
        }
        return True

    @classmethod
    def _extract_table_row(cls, node, line):
        headers = node['table']['headers']
        colspan = node['table']['colspan']

        row = dict()

        pre = line[:colspan[0][0]].strip()
        if pre:
            row['ord'] = cls.convert('ord', pre)

        for hdr in ('Number', 'Major', 'Minor', 'RaidDevice'):
            try:
                i = headers.index(hdr)
            except ValueError:
                pass
            else:
                (beg, end) = colspan[i]
                col = line[beg:end].strip()
                key = util.snake_case(hdr)
                row[key] = cls.convert(key, col)

        (beg, end) = colspan[headers.index('State')]
        templist = line[beg:].split()
        row['state'] = templist[:-1]
        row['device'] = templist[-1]

        return row

    @classmethod
    def _parse_table_row(cls, node, line):
        if not re.match(r'^\s*\w+(?:\s+\w+){5,}\s*', line):
            return False

        row = cls._extract_table_row(node, line)

        if 'rows' not in node['table']:
            node['table']['rows'] = []
        node['table']['rows'].append(row)
        return True

    @classmethod
    def _postprocess_mdadm_report_table(cls, node):
        if 'table' in node:
            node['device_list'] = node['table']['rows']
            del node['table']

    @classmethod
    def _parse_table_or_keyval(cls, state, node, line):
        if state['intable']:
            return cls._parse_table_row(node, line)
        elif cls._parse_table_header(node, line):
            state['intable'] = True
            return True
        else:
            return cls._parse_keyval(node, line)

    @classmethod
    def _parse_line(cls, state, node, line):
        if not node.get('device_name'):
            return cls._parse_device_name(node, line)
        else:
            return cls._parse_table_or_keyval(state, node, line)

    @classmethod
    def _parse_sheet(cls, nodes, sheet):
        state = {'intable': False}
        node = dict()
        for line in sheet:
            cls._parse_line(state, node, line)
        cls._postprocess_mdadm_report_table(node)
        nodes.append(node)

    @classmethod
    def _split_sheets(cls, report):
        sheets = []
        for line in report.splitlines():
            if cls._match_device_name(line):
                sheets.append([line])
            elif sheets:
                sheets[-1].append(line)
            else:
                # TODO: syntax error, issue a warning/error?
                return []
        return sheets

    @classmethod
    def _parse(cls, report, **kw):
        content = {'report': report, 'nodes': []}
        for sheet in cls._split_sheets(report):
            cls._parse_sheet(content['nodes'], sheet)
        return content


class MdadmDetailProbe(_MdadmBacktickProbe):

    @classmethod
    def flags(cls, flags, **kw):
        return ['--detail'] + flags


class MdadmExamineProbe(_MdadmBacktickProbe):

    @classmethod
    def flags(cls, flags, **kw):
        return ['--examine'] + flags


class MdadmProbe(composite_.CompositeProbe):

    @classmethod
    def new(cls, arguments=None, flags=None, **kw):
        """Creates a new instance of MdadmProbe for specified arguments by
           running and interpreting output of mdadm --detail, and
           mdadm --examine."""
        graph = cls.extract_lsblk_graph(arguments, flags, kw)

        devices = util.select_attr(graph.nodes, 'name', cls._is_raid)
        detail = MdadmDetailProbe.new(list(devices), flags, **kw)

        members = util.select_attr(graph.nodes, 'name', cls._is_member)
        examine = MdadmExamineProbe.new(list(members), flags, **kw)

        return cls({'detail': detail, 'examine': examine})

    @classmethod
    def probes(cls, **kw):
        internal = [MdadmDetailProbe, MdadmExamineProbe]
        return cls.mk_probes(internal, {'lsblkgraph': lsblk_.LsBlkProbe}, **kw)

    @classmethod
    def _is_raid(cls, item):
        return re.match(r'^raid(?:\d{1,2})$', item[1].type)

    @classmethod
    def _is_member(cls, item):
        return item[1].fstype == 'linux_raid_member'


# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
