# -*- coding: utf8 -*-

from . import composite_
from . import lvs_
from . import pvs_
from . import vgs_
from . import lsblk_

from .. import util

__all__ = ('LvmProbe',)


class LvmProbe(composite_.CompositeProbe):

    @classmethod
    def new(cls, arguments=None, flags=None, **kw):
        """Creates a new instance of LvmProbe for specified arguments by
           running and interpreting output of pvs, lvs, and vgs commands."""
        graph = cls.extract_lsblk_graph(arguments, flags, kw)

        members = util.select_attr(graph.nodes, 'name', cls._is_member)
        pvs = pvs_.PvsProbe.new(list(members), flags, **kw)

        volumes = util.select_attr(graph.nodes, 'name', cls._is_volume)
        lvs = lvs_.LvsProbe.new(list(volumes), flags, **kw)

        array = lvs.content['report'][0]['lv']
        groups = set(lv['vg_name'] for lv in array)
        vgs = vgs_.VgsProbe.new(list(groups), flags, **kw)

        return cls({'pvs': pvs, 'lvs': lvs, 'vgs': vgs})

    @classmethod
    def probes(cls, **kw):
        internal = [lvs_.LvsProbe, pvs_.PvsProbe, vgs_.VgsProbe]
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
