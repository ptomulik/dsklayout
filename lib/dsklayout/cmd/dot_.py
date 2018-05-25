# -*- coding: utf8 -*-
"""Provides the DotCmd class
"""

from . import cmd_

from ..archive import *
from ..cmd import *
from ..probe import *

import sys
import re

try:
    import graphviz
except ImportError as e:
    _has_graphviz = False
else:
    _has_graphviz = True


__all__ = ('DotCmd',)


class DotCmd(cmd_.Cmd):

    __slots__ = ()

    def _probe(self, klass, tool, args, kw=None):
        kwargs = dict({tool: self.getarg(tool, tool)}, **(kw or {}))
        return klass.new(*args, **kwargs)

    def _lsblk_probe(self, devices=None):
        return self._probe(LsBlkProbe, 'lsblk', (devices,))

    def _lsblk_graph(self, devices=None):
        return self._lsblk_probe(devices).graph()

    def _newgraph(self):
        infile = self.getarg('input')
        if infile is not None:
            with Archive.new(infile, 'r') as archive:
                graph = archive.metadata.graph
        else:
            graph = self._lsblk_graph(self.getarg('devices'))
        return graph

    @classmethod
    def _dot_id(cls, string):
        ident = re.sub(r'\W', '_', string)
        if not ident or not re.match(r'[a-zA-Z_]', ident[0]):
            ident = '_' . ident
        return ident


    def _dot_node_label(self, node):
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

    def _dot_node(self, dot, graph, node):
        label = self._dot_node_label(graph.node(node))
        dot.node(self._dot_id(node), label)

    def _dot_edge(self, dot, graph, edge):
        dot.edge(self._dot_id(edge[0]), self._dot_id(edge[1]))

    def _dot_build(self, dot):
        graph = self._newgraph()
        for node in graph.nodes:
            self._dot_node(dot, graph, node)
        for edge in graph.edges:
            self._dot_edge(dot, graph, edge)

    def _dot_output(self, dot):
        if self.getarg('view'):
            dot.view()
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
