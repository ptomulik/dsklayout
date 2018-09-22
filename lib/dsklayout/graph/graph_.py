# -*- coding: utf8 -*-

from . import edges_
from . import nodes_
from . import elems_
from .. import util

__all__ = ('Graph',)

MISSING = elems_.MISSING


class Graph:
    """Represents a directed graph of block devices"""

    __slots__ = ('_nodes', '_edges')

    def __init__(self, nodes=(), edges=(), **kw):
        nodes = nodes_.Nodes(nodes, **kw)
        edges = edges_.Edges(edges, **kw)
        if kw.get('consistency', True):
            _consistency(nodes, edges)
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
        name = self.__class__.__name__
        return "%s(%s, %s)" % (name, repr(self._nodes), repr(self._edges))

    def add_node(self, node, data=MISSING):
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

    def add_edge(self, edge, data=MISSING, **kw):
        """Add edge and its nodes to graph."""
        left, right = tuple(edge)
        self._edges.add(edge, data)
        self.add_node(left, kw.get(left, MISSING))
        self.add_node(right, kw.get(right, MISSING))

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
        return _select_related(self._nodes, self._edges.successors, node)

    def predecessors(self, node):
        """Returns predecessors of the given node."""
        return _select_related(self._nodes, self._edges.predecessors, node)

    def neighbors(self, node):
        """Returns a set of nodes that are connected to a given node"""
        return _select_related(self._nodes, self._edges.neighbors, node)

    def outward(self, node):
        """Returns edges outward to given node"""
        return _select_related(self._nodes, self._edges.outward, node)

    def inward(self, node):
        """Returns edges inward to given node"""
        return _select_related(self._nodes, self._edges.inward, node)

    def incident(self, node):
        """Returns edges incident to given node"""
        return _select_related(self._nodes, self._edges.incident, node)

    @classmethod
    def adjacent(cls, node, edge):
        """Returns a node on the opposite end of edge"""
        return edges_.Edges.adjacent(node, edge)

    def roots(self):
        """Returns a set of root nodes (having no predecessors)"""
        return _select_not_satisfying(self._nodes, self.has_predecessors)

    def leafs(self):
        """Returns a set of leaf nodes (having no successors)"""
        return _select_not_satisfying(self._nodes, self.has_successors)

    def isolated(self):
        """Returns a set of isolated nodes (having no neighbors)"""
        return _select_not_satisfying(self._nodes, self.has_neighbors)

    def dump_attributes(self):
        return {'nodes': util.dump_object(self.nodes),
                'edges': util.dump_object(self.edges)}

    @classmethod
    def load_attributes(cls, attributes):
        nodes = util.load_object(attributes['nodes'])
        edges = util.load_object(attributes['edges'])
        return cls(nodes, edges)


def _consistency(nodes, edges):
    """Checks provided nodes and edges for consistency"""
    # For each edge ensure, that their both endpoints refer existing nodes
    for (left, right) in edges:
        if left not in nodes:
            raise KeyError(left)
        if right not in nodes:
            raise KeyError(right)


def _select_related(nodes, selector, node):
    """Helper used to select node-related elements (nodes, edges)"""
    try:
        elems = selector(node)
    except KeyError:
        nodes[node]  # rethrow if we have no such node
        elems = ()   # otherwise it was an isolated node
    return set(elems)


def _select_not_satisfying(elems, condition):
    return {n for n in elems if not condition(n)}


# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
