# -*- coding: utf8 -*-
"""Provides the DotCmd class
"""

from . import cmd_

from ..archive import *
from ..cmd import *
from ..probe import *

import sys
import re
import tempfile

try:
    import graphviz
except ImportError as e:
    _has_graphviz = False
else:
    _has_graphviz = True


__all__ = ('DotCmd',)


class DotCmd(cmd_.Cmd):

    __slots__ = ('_lsblk_graph',)

    def _probe(self, klass, tool, args, kw=None):
        kwargs = dict({tool: self.getarg(tool, tool)}, **(kw or {}))
        return klass.new(*args, **kwargs)

    def _lsblk_probe(self, devices=None):
        return self._probe(LsBlkProbe, 'lsblk', (devices,))


    def _new_lsblk_graph(self):
        infile = self.getarg('input')
        if infile is not None:
            with Archive.new(infile, 'r') as archive:
                graph = archive.metadata.graph
        else:
            graph = self._lsblk_probe(self.getarg('devices')).graph()
        return graph

    @property
    def lsblk_graph(self):
        if not hasattr(self, '_lsblk_graph'):
            self._lsblk_graph = self._new_lsblk_graph()
        return self._lsblk_graph

    def _dot_lsblk_node_label(self, node):
        extra = [node.mountpoint, node.partlabel, node.fstype]
        extra = [s for s in extra if s]
        if extra and extra[0] != node.name:
            label = "%s (%s)" % (node.name, extra[0])
        else:
            label = node.name
        return label

    def _dot_setattr(self, dot):
        dot.attr(splines='ortho', nodesep='0.75')
        dot.edge_attr.update(arrowhead='vee', arrowtail='vee')
        dot.node_attr.update(shape='rect')

    def _dot_add_lsblk_node(self, dot, graph, node):
        label = self._dot_lsblk_node_label(graph.node(node))
        dot.node(node, label)

    def _dot_add_lsblk_edge(self, dot, graph, edge):
        dot.edge(edge[0], edge[1])

    def _dot_add_lvm_vg(self, dot, vg):
        name = vg['vg_name']
        dot.node(name)

    def _dot_add_lvm_pv(self, dot, pv):
        name = pv['pv_name']
        dot.node(name)
        try:
            vg = pv['vg_name']
        except KeyError:
            pass
        else:
            dot.edge(name, vg)

    def _dot_lvm_lv_label(self, lv):
        if lv.get('lv_dm_path'):
            return "%s (%s)" % (lv['lv_name'], lv['lv_path'])
        elif lv.get('lv_path'):
            return "%s (%s)" % (lv['lv_name'], lv['lv_dm_path'])
        else:
            return lv['lv_name']

    def _dot_add_lvm_lv(self, dot, lv):
        name = lv['lv_name']
        label = self._dot_lvm_lv_label(lv)
        dot.node(name, label)
        try:
            vg = lv['vg_name']
        except KeyError:
            pass
        else:
            dot.edge(vg, name)

    def _dot_build_lsblk(self, dot):
        kw = {'name': 'cluster_lsblk',
              'comment': 'Block-device graph created with lsblk',
              'body': ['\tlabel = "LSBLK"']}
        with dot.subgraph(**kw) as sg:
            graph = self.lsblk_graph
            for node in graph.nodes:
                self._dot_add_lsblk_node(sg, graph, node)
            for edge in graph.edges:
                self._dot_add_lsblk_edge(sg, graph, edge)

    def _dot_build_lvm(self, dot):
        graph = self.lsblk_graph
        members = [graph.node(n).name for n in graph.nodes
                   if graph.node(n).fstype == 'LVM2_member']
        volumes = [graph.node(n).name for n in graph.nodes
                   if graph.node(n).type == 'lvm']
        if members or volumes:
            pvs = PvsProbe.new(members).content['report'][0]['pv']
            lvs = LvsProbe.new(volumes).content['report'][0]['lv']
            groups = list(set(lv['vg_name'] for lv in lvs))
            vgs = VgsProbe.new(groups).content['report'][0]['vg']
            kw = {'name': 'cluster_lvm',
                  'comment': 'LVM graph',
                  'body': ['\tcolor=black',
                           '\tlabel="LVM"']}
            with dot.subgraph(**kw) as sg:
                for vg in vgs:
                    self._dot_add_lvm_vg(sg, vg)
                for pv in pvs:
                    self._dot_add_lvm_pv(sg, pv)
                for lv in lvs:
                    self._dot_add_lvm_lv(sg, lv)

    def _dot_build(self, dot):
        self._dot_build_lsblk(dot)
        self._dot_build_lvm(dot)

    def _dot_output(self, dot):
        if self.getarg('view'):
            dot.view(cleanup=True)
        else:
            outfile = self.getarg('output')
            if outfile is None or output == '-':
                sys.stdout.write(dot.source + "\n")
            else:
                dot.save(outfile)

    def _dot(self, dot):
        self._dot_setattr(dot)
        self._dot_build(dot)
        self._dot_output(dot)
        return 0

    def run(self):
        if not _has_graphviz:
            # FIXME: elaborate better error reporting
            sys.stderr.write("error: missing graphviz package\n")
            return 1
        return self._dot(graphviz.Digraph())


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
