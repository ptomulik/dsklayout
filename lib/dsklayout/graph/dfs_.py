# -*- coding: utf8 -*-

from . import trail_
from . import traversal_

import collections

__all__ = ('Dfs',)


class Dfs(traversal_.Traversal):
    """Deep-First Search algorithm"""

    __slots__ = ()

    def __init__(self, **kw):
        super().__init__(**kw)

    def __call__(self, graph, start_nodes, **kw):
        trail = trail_.Trail(graph, **self.callbacks(**kw))
        for start_node in start_nodes:
            if trail.node_explored(start_node):
                continue
            if self._dfs(trail, start_node, None):
                break
        return trail

    def _dfs(self, trail, node, edge):
        trail.explore_and_append_node(node)
        stop = self._invoke_callback(trail.ingress_func, trail, node, edge)
        if not stop:
            stop = self._select_edges_and_iterate(trail, node)
        stop |= self._invoke_callback(trail.egress_func, trail, node, edge)
        return stop

    def _select_edges_and_iterate(self, trail, node):
        for edge in self.select_edges(trail.graph, node):
            if trail.edge_explored(edge):
                continue
            adjacent_node = trail.graph.adjacent(node, edge)
            if self._handle_adjacent_node(trail, adjacent_node, edge):
                return True
        return False

    def _handle_adjacent_node(self, trail, adjacent_node, edge):
        if not trail.node_explored(adjacent_node):
            trail.explore_and_append_edge(edge)
            return self._dfs(trail, adjacent_node, edge)
        else:
            trail.explore_and_append_backedge(edge)
            return self._invoke_callback(trail.backedge_func, trail, edge)

    @classmethod
    def _invoke_callback(cls, func, trail, elem, *args):
        if func(trail.graph, elem, *args):
            if trail.result is None:
                trail.result = elem
            return True
        else:
            return False

# vim: set ft=python et ts=4 sw=4:
