# -*- coding: utf8 -*-

from . import backtick_
from . import composite_
from . import lsblk_

from .. import util

import abc

__all__ = ('LvsProbe', 'VgsProbe', 'PvsProbe', 'LvmProbe')


class _LvmReportProbe(backtick_.BackTickProbe):

    @classmethod
    @abc.abstractmethod
    def cmdname(cls):
        pass

    @classmethod
    def xflags(cls):
        return []

    @classmethod
    def command(cls, **kw):
        return kw.get(cls.cmdname, cls.cmdname)

    @classmethod
    def flags(cls, flags, **kw):
        return ['--readonly', '--reportformat', 'json'] + cls.xflags() + flags

    @classmethod
    def parse(cls, output):
        return json.loads(output)


class LvsProbe(_LvmReportProbe):

    @classmethod
    def cmdname(cls):
        return 'lvs'

    @classmethod
    def xflags(cls):
        return ['-o', '+lv_all']


class PvsProbe(_LvmReportProbe):

    @classmethod
    def cmdname(cls):
        return 'pvs'

    @classmethod
    def xflags(cls):
        return ['-o', '+vg_all']


class VgsProbe(_LvmReportProbe):

    @classmethod
    def cmdname(cls):
        return 'vgs'


class LvmProbe(composite_.CompositeProbe):

    @classmethod
    def new(cls, arguments=None, flags=None, **kw):
        """Creates a new instance of LvmProbe for specified arguments by
           running and interpreting output of pvs, lvs, and vgs commands."""
        graph = cls.extract_lsblk_graph(arguments, flags, kw)

        members = util.select_attr(graph.nodes, 'name', cls._is_member)
        pvs = PvsProbe.new(list(members), flags, **kw)

        volumes = util.select_attr(graph.nodes, 'name', cls._is_volume)
        lvs = LvsProbe.new(list(volumes), flags, **kw)

        array = lvs.content['report'][0]['lv']
        groups = set(lv['vg_name'] for lv in array)
        vgs = VgsProbe.new(list(groups), flags, **kw)

        return cls({'pvs': pvs, 'lvs': lvs, 'vgs': vgs})

    @classmethod
    def probes(cls, **kw):
        internal = [LvsProbe, PvsProbe, VgsProbe]
        return cls.mk_probes(internal, {'lsblkgraph': lsblk_.LsBlkProbe}, **kw)

    @classmethod
    def _is_member(cls, item):
        return item[1].fstype == 'LVM_member'

    @classmethod
    def _is_volume(cls, item):
        return item[1].type == 'lvm'


# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
