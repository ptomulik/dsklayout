# -*- coding: utf8 -*-

from . import composite_
from . import lvs_
from . import pvs_
from . import vgs_
from . import lsblk_

__all__ = ('LvmProbe',)


class LvmProbe(composite_.CompositeProbe):

    @classmethod
    def new(cls, arguments=None, flags=None, **kw):
        """Creates a new instance of LvmProbe for specified arguments by
           running and interpreting output of pvs, lvs, and vgs commands."""
        graph = cls.mk_lsblk_graph(arguments, flags, kw)
        members = cls.select_node_names(graph.nodes, cls._is_member)
        volumes = cls.select_node_names(graph.nodes, cls._is_volume)
        pvs = pvs_.PvsProbe.new(members, flags, **kw)
        lvs = lvs_.LvsProbe.new(volumes, flags, **kw)
        array = lvs.content['report'][0]['lv']
        groups = list(set(lv['vg_name'] for lv in array))
        vgs = vgs_.VgsProbe.new(groups, flags, **kw)
        return cls({'pvs': pvs, 'lvs': lvs, 'vgs': vgs})

    @classmethod
    def probes(cls, **kw):
        internal = [lvs_.LvsProbe, pvs_.PvsProbe, vgs_.VgsProbe]
        return cls.mk_probes(internal, {'lsblkgraph': lsblk_.LsBlkProbe}, **kw)

    @classmethod
    def _is_member(cls, node):
        return node.fstype == 'LVM_member'

    @classmethod
    def _is_volume(cls, node):
        return node.type == 'lvm'


# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
