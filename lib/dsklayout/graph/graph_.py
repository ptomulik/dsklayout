# -*- coding: utf8 -*-

from . import edges_
from . import nodes_
from . import elems_

__all__ = ( 'Graph', )

_missing = elems_._missing

class Graph(object):
    """Represents a directed graph of block devices"""

    __slots__ = ( '_nodes', '_edges' )

    def __init__(self, nodes=(), edges=(), **kw):
        nodes = nodes_.Nodes(nodes, **kw)
        edges = edges_.Edges(edges, **kw)
        if kw.get('consistency', True):
            self._consistency(nodes, edges)
        self._nodes = nodes
        self._edges = edges

    @property
    def nodes(self):
        """All nodes in the graph"""
        return self._nodes

    @property
    def edges(self):
        """All edges in the graph"""
        return self._edges

    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__.__name__, repr(self._nodes), repr(self._edges))

    def add_node(self, node, data=_missing):
        """Add new node to graph"""
        self._nodes.add(node, data)

    def del_node(self, node):
        """Deletes node and all its incident edges"""
        del self._nodes[node]
        self._edges.del_incident(node)

    def discard_node(self, node):
        """Discards node and all its incident edges"""
        if node in self._nodes:
            self.del_node(node)

    def has_node(self, node):
        """Returns True if the graph has given node"""
        return node in self._nodes

    def node(self, node):
        """Returns data assigned to node. Same as ``self.nodes[node]``"""
        return self._nodes[node]

    def add_edge(self, edge, data=_missing, **kw):
        """Add edge and its nodes to graph."""
        left, right = tuple(edge)
        self._edges.add(edge, data)
        self.add_node(left, kw.get(left, _missing))
        self.add_node(right, kw.get(right, _missing))

    def del_edge(self, edge):
        """Deletes edge leaving its (possibly isolated) nodes in graph."""
        del self._edges[edge]

    def discard_edge(self, edge):
        """Discards edge leaving its (possibly isolated) nodes in graph."""
        self._edges.discard(edge)

    def has_edge(self, edge):
        """Returns True if the graph has given edge"""
        return edge in self._edges

    def edge(self, edge):
        """Returns data assigned to edge. Same as ``self.edges[edge]``"""
        return self._edges[edge]

    def has_successors(self, node):
        """Returns True if node has successors."""
        return self._edges.has_successors(node)

    def has_predecessors(self, node):
        """Returns True if node has predecessors."""
        return self._edges.has_predecessors(node)

    def has_neighbors(self, node):
        """Returns True if node has neighbors."""
        return self._edges.has_neighbors(node)

    def successors(self, node):
        """Returns successors of the given node."""
        return self._select_node_related(self._edges.successors, node)

    def predecessors(self, node):
        """Returns predecessors of the given node."""
        return self._select_node_related(self._edges.predecessors, node)

    def neighbors(self, node):
        """Returns a set of nodes that are connected to a given node"""
        return self._select_node_related(self._edges.neighbors, node)

    def outward(self, node):
        """Returns edges outward to given node"""
        return self._select_node_related(self._edges.outward, node)

    def inward(self, node):
        """Returns edges inward to given node"""
        return self._select_node_related(self._edges.inward, node)

    def incident(self, node):
        """Returns edges incident to given node"""
        return self._select_node_related(self._edges.incident, node)

    def _select_node_related(self, selector, node):
        """Helper used to select node-related elements (nodes, edges)"""
        try:
            elems = selector(node)
        except KeyError:
            self._nodes[node] # rethrow if we have no such node
            elems = () # otherwise it was an isolated node
        return set(elems)

    @classmethod
    def adjacent(cls, node, edge):
        """Given an edge and a node returns the node on the other end of edge"""
        return edges_.Edges.adjacent(node, edge)

    def roots(self):
        """Returns a set of root nodes (having no predecessors)"""
        return { n for n in self._nodes if not self.has_predecessors(n) }

    def leafs(self):
        """Returns a set of leaf nodes (having no successors)"""
        return { n for n in self._nodes if not self.has_successors(n) }

    def isolated(self):
        """Returns a set of isolated nodes"""
        return { n for n in self._nodes if not self.has_predecessors(n) and not self.has_successors(n) }

    def _consistency(self, nodes, edges):
        """Checks provided nodes and edges for consistency"""
        # For each edge ensure, that their both endpoints refer existing nodes
        for (left, right) in edges:
            if left not in nodes:
                raise KeyError(left)
            if right not in nodes:
                raise KeyError(right)


# vim: set ft=python et ts=4 sw=4:
