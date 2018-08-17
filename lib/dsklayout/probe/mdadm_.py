# -*- coding: utf8 -*-

from . import probe_
from . import backtick_
from . import lsblk_

import re

__all__ = ('MdadmDetailProbe', 'MdadmExamineProbe', 'MdadmProbe')


def _select_nodes(graph, func):
    return [graph.node(n).name for n in graph.nodes if func(graph.node(n))]


class _MdadmReportProbe(backtick_.BackTickProbe):

    @classmethod
    def command(cls, **kw):
        return kw.get('mdadm', 'mdadm')

    @classmethod
    def parse(cls, output):
        return cls._parse(output)

    @classmethod
    def _parse_device_name(cls, content, line):
        m = re.match(r'^\s*(/+\w+(?:/+\w+)*):\s*$', line)
        if not m:
            return False
        content['Device Name'] = m.group(1)
        return True

    @classmethod
    def _parse_keyval(cls, content, line):
        m = re.match(r'^\s*(\w+(?:\s+\w+)*)\s*:\s*(\S+(?:\s+\S+)*)\s*$', line)
        if not m:
            return False
        content[m.group(1)] = m.group(2)
        return True

    @classmethod
    def _parse_table_header(cls, content, line):
        m = re.match(r'^\s*(Number)\s+(Major)\s+(Minor)\s+(RaidDevice)\s+(State)\s*$', line)
        if not m:
            return False
        content['table'] = {
            'headers': m.groups(),
            'colspan': [m.span(i) for i in range(1, 1+len(m.groups()))]
        }
        return True

    @classmethod
    def _parse_table_row(cls, content, line):
        headers = content['table']['headers']
        colspan = content['table']['colspan']

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

        if 'rows' not in content['table']:
            content['table']['rows'] = []
        content['table']['rows'].append(row)
        return True

    @classmethod
    def _postprocess_mdadm_report_table(cls, content):
        if 'table' in content:
            content['Device List'] = content['table']['rows']
            del content['table']

    @classmethod
    def _parse_line(cls, state, content, line):
        if not content.get('Device Name'):
            return cls._parse_device_name(content, line)
        elif state['intable']:
            return cls._parse_table_row(content, line)
        else:
            if cls._parse_table_header(content, line):
                state['intable'] = True
                return True
            else:
                return cls._parse_keyval(content, line)

    @classmethod
    def _parse(cls, report, **kw):
        state = {'intable': False}
        content = {'Report': report}
        for line in report.splitlines():
            cls._parse_line(state, content, line)
        cls._postprocess_mdadm_report_table(content)
        return content


class MdadmDetailProbe(_MdadmReportProbe):

    @classmethod
    def flags(cls, flags, **kw):
        return ['--detail'] + flags


class MdadmExamineProbe(_MdadmReportProbe):

    @classmethod
    def flags(cls, flags, **kw):
        return ['--examine'] + flags


class MdadmProbe(probe_.Probe):

    @classmethod
    def _lsblk_graph(cls, arguments, flags, kw):
        try:
            graph = kw['lsblkgraph']
            del kw['lsblkgraph']
        except KeyError:
            graph = lsblk_.LsBlkProbe.new(arguments, flags, **kw).graph()
        return graph

    @classmethod
    def new(cls, arguments=None, flags=None, **kw):
        """Creates a new instance of MdadmProbe for specified arguments by
           running and interpreting output of mdadm --detail, and
           mdadm --examine."""
        graph = cls._lsblk_graph(arguments, flags, kw)
        devices = _select_nodes(graph, lambda n : re.match(r'^raid(?:\d{1,2})$', n.type) )
        members = _select_nodes(graph, lambda n : n.fstype == 'linux_raid_member')

        devices = {dev: MdadmDetailProbe.new(dev, flags, **kw).content
                   for dev in devices}
        members = {mem: MdadmExamineProbe.new(mem, flags, **kw).content
                   for mem in members}
        return cls({'devices': devices, 'members': members})

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
