# -*- coding: utf8 -*-

from . import probe_
from . import lvs_
from . import pvs_
from . import vgs_
from . import lsblk_

__all__ = ('LvmProbe',)


def _select_nodes(graph, func):
    return [graph.node(n).name for n in graph.nodes if func(graph.node(n))]


class LvmProbe(probe_.Probe):

    @classmethod
    def new(cls, arguments=None, flags=None, **kw):
        """Creates a new instance of LvmProbe for specified arguments by
           running and interpreting output of pvs, lvs, and vgs commands."""
        graph = cls._lsblk_graph(arguments, flags, kw)
        members = _select_nodes(graph, lambda n : n.fstype == 'LVM_member')
        volumes = _select_nodes(graph, lambda n : n.type == 'lvm')
        pvs = pvs_.PvsProbe.new(members, flags, **kw)
        lvs = lvs_.LvsProbe.new(volumes, flags, **kw)
        groups = list(set(lv['vg_name'] for lv in lvs))
        vgs = vgs_.VgsProbe.new(groups, flags, **kw)
        return cls({'pvs': pvs, 'lvs': lvs, 'vgs': vgs})

    @classmethod
    def available(cls, **kw):
        probes = [lvs_.LvsProbe, pvs_.PvsProbe, vgs_.VgsProbe]
        if 'lsblkgraph' not in kw:
            probes.append(lsblk_.LsBlkProbe)
        return all(p.available(**kw) for p in probes)

    @classmethod
    def _lsblk_graph(cls, arguments, flags, kw):
        try:
            graph = kw['lsblkgraph']
            del kw['lsblkgraph']
        except KeyError:
            graph = lsblk_.LsBlkProbe.new(arguments, flags, **kw).graph()
        return graph


# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
