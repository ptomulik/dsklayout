# -*- coding: utf8 -*-
"""Provides the DotCmd class
"""

from . import cmd_

from ..archive import *
from ..cmd import *
from ..device import *
from ..graph import *
from ..probe import *
from ..visitor import *

import sys
import re


__all__ = ('DotCmd',)

class _Dot:
    __slots__ = ('_nodes', '_edges', '_attributes')

    def __init__(self, nodes=None, edges=None, attributes=None):
        self._nodes = nodes or []
        self._edges = edges or []
        self._attributes = attributes or self.default_attributes()

    @property
    def nodes(self):
        return self._nodes

    @property
    def edges(self):
        return self._edges

    @property
    def attributes(self):
        return self._attributes

    def add_node(self, graph, node):
        ident = self.to_id(node)
        node = graph.node(node)
        extra = [node.mountpoint, node.partlabel, node.name]
        extra = [s for s in extra if s]
        if extra and extra[0] != node.kname:
            label = "%s (%s)" % (node.kname, extra[0])
        else:
            label = node.kname
        self._nodes.append("%s [label=\"%s\"]" % (ident, label))

    def add_edge(self, graph, e):
        self._edges.append("%s -> %s" % (self.to_id(e[0]), self.to_id(e[1])))

    def _gen_stmt_list(self):
        return ";\n  ".join(self.attributes + self.nodes + self.edges)

    def _gen_graph(self):
        return "%s {\n  %s\n}" % (self.graph_type(), self._gen_stmt_list())

    def to_string(self):
        return self._gen_graph()

    @classmethod
    def to_id(cls, s):
        ident = re.sub(r'\W', '_', s)
        if not ident or not re.match(r'[a-zA-Z_]', ident[0]):
            ident = '_' . ident
        return ident

    @classmethod
    def graph_type(cls):
        return "digraph"

    @classmethod
    def default_attributes(cls):
        return ['graph [splines=ortho, nodesep="0.75"]',
                'edge [arrowhead=vee, arrowtail=vee]',
                'node [shape=rect]']

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

    def _fill_dot(self, dot):
        graph = self._newgraph()
        for node in graph.nodes:
            dot.add_node(graph, node)
        for edge in graph.edges:
            dot.add_edge(graph, edge)

    def _output_dot(self, dot):
        outfile = self.getarg('output')
        if outfile is None or output == '-':
            sys.stdout.write(dot.to_string() + "\n")
        else:
            with open(outfile, 'w') as f:
                f.write(dot.to_string() + "\n")

    def _dot(self, dot):
        self._fill_dot(dot)
        self._output_dot(dot)
        return 0

    def run(self):
        return self._dot(_Dot())


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
