# -*- coding: utf8 -*-

from . import composite_
from . import backtick_
from . import lsblk_

from .. import util

import re

__all__ = ('MdadmDetailProbe', 'MdadmExamineProbe', 'MdadmProbe')


class _MdadmReportProbe(backtick_.BackTickProbe):

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
        node['Device Name'] = m.group(1)
        return True

    @classmethod
    def _parse_keyval(cls, node, line):
        m = re.match(r'^\s*(\w+(?:\s+\w+)*)\s*:\s*(\S+(?:\s+\S+)*)\s*$', line)
        if not m:
            return False
        node[m.group(1)] = m.group(2)
        return True

    @classmethod
    def _parse_table_header(cls, node, line):
        m = re.match(r'^\s*(Number)\s+(Major)\s+(Minor)\s+(RaidDevice)\s+(State)\s*$', line)
        if not m:
            return False
        node['table'] = {
            'headers': m.groups(),
            'colspan': [m.span(i) for i in range(1, 1+len(m.groups()))]
        }
        return True

    @classmethod
    def _parse_table_row(cls, node, line):
        headers = node['table']['headers']
        colspan = node['table']['colspan']

        m = re.match(r'^\s*\w+(?:\s+\w+){5,}\s*', line)
        if not m:
            return False

        row = dict()

        pre = line[:colspan[0][0]].strip()
        if pre:
            row['Ord'] = pre

        for key in ('Number', 'Major', 'Minor', 'RaidDevice'):
            try:
                i = headers.index(key)
            except ValueError:
                pass
            else:
                (beg, end) = colspan[i]
                col = line[beg:end].strip()
                row[key] = col

        (beg, end) = colspan[headers.index('State')]
        templist = line[beg:].split()
        row['State'] = templist[:-1]
        row['Device'] = templist[-1]

        if 'rows' not in node['table']:
            node['table']['rows'] = []
        node['table']['rows'].append(row)
        return True

    @classmethod
    def _postprocess_mdadm_report_table(cls, node):
        if 'table' in node:
            node['Device List'] = node['table']['rows']
            del node['table']

    @classmethod
    def _parse_line(cls, state, node, line):
        if not node.get('Device Name'):
            return cls._parse_device_name(node, line)
        elif state['intable']:
            return cls._parse_table_row(node, line)
        else:
            if cls._parse_table_header(node, line):
                state['intable'] = True
                return True
            else:
                return cls._parse_keyval(node, line)

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
        content = {'Report': report, 'Nodes': []}
        for sheet in cls._split_sheets(report):
            cls._parse_sheet(content['Nodes'], sheet)
        return content


class MdadmDetailProbe(_MdadmReportProbe):

    @classmethod
    def flags(cls, flags, **kw):
        return ['--detail'] + flags


class MdadmExamineProbe(_MdadmReportProbe):

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

        devices = util.select_values_attr(graph.nodes, 'name', cls._is_raid)
        detail = MdadmDetailProbe.new(list(devices), flags, **kw)

        members = util.select_values_attr(graph.nodes, 'name', cls._is_member)
        examine = MdadmExamineProbe.new(list(members), flags, **kw)

        return cls({'detail': detail, 'examine': examine})

    @classmethod
    def probes(cls, **kw):
        internal = [MdadmDetailProbe, MdadmExamineProbe]
        return cls.mk_probes(internal, {'lsblkgraph': lsblk_.LsBlkProbe}, **kw)

    @classmethod
    def _is_raid(cls, node):
        return re.match(r'^raid(?:\d{1,2})$', node.type)

    @classmethod
    def _is_member(cls, node):
        return node.fstype == 'linux_raid_member'


# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
