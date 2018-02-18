# -*- coding: utf8 -*-

from . import trail_
from . import traversal_

import collections

__all__ = ( 'Dfs', )

class Dfs(traversal_.Traversal):
    """Deep-First Search algorithm"""

    __slots__ = ( )

    def __init__(self, **kw):
        super().__init__(**kw)

    def __call__(self, graph, start_nodes, **kw):
        trail = trail_.Trail(graph)
        stop = False
        for start_node in start_nodes:
            if not stop and not trail.node_explored(start_node):
                stop = self._dfs(trail, start_node, None, **self.callbacks(**kw))
        return trail

    def _dfs(self, trail, node, last_edge, enter_func, leave_func, backedge_func):
        trail.explore_and_append_node(node)
        stop = self._invoke_elem_callback(enter_func, trail, node, last_edge)
        if not stop:
            for edge in self.select_edges(trail.graph, node):
                if not trail.edge_explored(edge):
                    adjacent_node = trail.graph.adjacent(node, edge)
                    if not trail.node_explored(adjacent_node):
                        trail.explore_and_append_edge(edge)
                        stop = self._dfs(trail, adjacent_node, edge, enter_func, leave_func, backedge_func)
                    else:
                        trail.explore_and_append_backedge(edge)
                        stop = self._invoke_elem_callback(backedge_func, trail, edge)
                    if stop: break
        stop |= self._invoke_elem_callback(leave_func, trail, node, last_edge)
        return stop

    @classmethod
    def _invoke_elem_callback(cls, func, trail, elem, *args):
        if func(trail.graph, elem, *args):
            if trail.result is None:
                trail.result = elem
            return True
        else:
            return False

# vim: set ft=python et ts=4 sw=4:
