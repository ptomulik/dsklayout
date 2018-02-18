# -*- coding: utf8 -*-

from . import elems_

import collections.abc

__all__ = ( 'Edges', )

class Edges(elems_.Elems):
    """An unordered set of graph edges. An edge is a tuple of hashable objects.

       In addition to the ordinary set, this class maintains two dictionaries
       that resemble forward and backward relations between nodes.
    """

    __slots__ = ( '_successors_dict', '_predecessors_dict' )

    def __init__(self, items = (), **kw):
        self._successors_dict = dict()
        self._predecessors_dict = dict()
        if 'edgedata' in kw: kw['data'] = kw['edgedata']
        super().__init__(items, **kw)

    @property
    def successors_dict(self):
        """Returns the dictionary of outward nodes"""
        return self._successors_dict

    @property
    def predecessors_dict(self):
        """Returns the dictionary of inward nodes"""
        return self._predecessors_dict

    def has_successors(self, node):
        """Returns True if node has successors"""
        return node in self._successors_dict

    def has_predecessors(self, node):
        """Returns True if node has predecessors"""
        return node in self._predecessors_dict

    def has_neighbors(self, node):
        """Returns True if node appears anywhere in edges"""
        return node in self._successors_dict or node in self._predecessors_dict

    def successors(self, node):
        """Returns a set of successors of a given node"""
        return self._select_node_related_elems(self._successors_dict, self._predecessors_dict, node)

    def predecessors(self, node):
        """Returns a set of predecessors of a given node"""
        return self._select_node_related_elems(self._predecessors_dict, self._successors_dict, node)

    def neighbors(self, node):
        """Returns a set of nodes that are connected to a given node"""
        return self.predecessors(node) | self.successors(node)

    def outward(self, node):
        """Returns a set of outward edges for given node"""
        return { (node,s) for s in self.successors(node) }

    def inward(self, node):
        """Returns a set of inward edges for given node"""
        return { (p,node) for p in self.predecessors(node) }

    def incident(self, node):
        """Returns a set of edges incident (outward or inward) to a given node"""
        return self.outward(node) | self.inward(node)

    @classmethod
    def adjacent(self, node, edge):
        """Given an edge and a node returns the node on the other end of edge"""
        left, right = tuple(edge)
        if left == node:
            return right
        elif right == node:
            return left
        else:
            raise KeyError(node)

    def __contains__(self, edge):
        return super().__contains__(tuple(edge))

    def __getitem__(self, edge):
        try:
            return super().__getitem__(tuple(edge))
        except KeyError:
            raise KeyError(edge)

    def __delitem__(self, edge):
        try:
            left, right = tedge = tuple(edge)
        except ValueError:
            raise KeyError(edge) # it would not be found, anyway
        try:
            super().__delitem__(tedge)
        except KeyError:
            raise KeyError(edge)
        self._discard_neighbor(self._successors_dict, left, right)
        self._discard_neighbor(self._predecessors_dict, right, left)

    def add(self, edge, data=elems_._missing):
        left, right = tedge = tuple(edge)
        super().add(tedge, data)
        self._add_neighbor(self._successors_dict, left, right)
        self._add_neighbor(self._predecessors_dict, right, left)

    def clear(self):
        super().clear()
        self._successors_dict.clear()
        self._predecessors_dict.clear()

    def del_incident(self, node):
        """Delete all edges incident to a node"""
        for edge in self.incident(node):
            del self[edge]

    @classmethod
    def _select_node_related_elems(cls, related, opposite, node):
        try:
            nodes = related[node]
        except KeyError:
            opposite[node] # throw, if 'node' doesn't appear in any of the dictionaries
            nodes = set() # otherwise return an empty set
        return nodes

    @classmethod
    def _discard_neighbor(cls, registry, node, neighbor):
        registry[node].discard(neighbor)
        if not registry[node]:
            del registry[node]

    @classmethod
    def _add_neighbor(cls, registry, node, neighbor):
        if node not in registry:
            registry[node] = set()
        registry[node].add(neighbor)


# vim: set ft=python et ts=4 sw=4:
