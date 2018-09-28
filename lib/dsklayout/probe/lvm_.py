# -*- coding: utf8 -*-

from . import backtick_
from . import composite_
from . import lsblk_

from .. import util

import abc
import json

__all__ = ('LvsProbe', 'VgsProbe', 'PvsProbe', 'LvmProbe')


class _LvmBacktickProbe(backtick_.BackTickProbe):

    @classmethod
    def xflags(cls):
        return []

    @classmethod
    def flags(cls, flags, **kw):
        return ['--readonly', '--reportformat', 'json'] + cls.xflags() + flags

    @classmethod
    def parse(cls, text):
        return json.loads(text)


class LvsProbe(_LvmBacktickProbe):

    @classmethod
    def cmdname(cls):
        return 'lvs'

    @classmethod
    def xflags(cls):
        return ['-o', '+lv_all']


class PvsProbe(_LvmBacktickProbe):

    @classmethod
    def cmdname(cls):
        return 'pvs'

    @classmethod
    def xflags(cls):
        return ['-o', '+pv_all']


class VgsProbe(_LvmBacktickProbe):

    @classmethod
    def cmdname(cls):
        return 'vgs'

    @classmethod
    def xflags(cls):
        return ['-o', '+vg_all']


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
    def uses(cls, **kw):
        internal = [LvsProbe, PvsProbe, VgsProbe]
        return cls.mk_uses(internal, {'lsblkgraph': lsblk_.LsBlkProbe}, **kw)

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
