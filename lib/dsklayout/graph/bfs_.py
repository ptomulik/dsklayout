# -*- coding: utf8 -*-

from . import trail_
from . import traversal_

import collections

__all__ = ( 'Bfs', )

class Bfs(traversal_.Traversal):
    """Bread-First Search algorithm"""

    __slots__ = ( )

    def __init__(self, **kw):
        super().__init__(**kw)

    def __call__(self, graph, start_nodes, **kw):
        trail = trail_.Trail(graph)
        for start_node in start_nodes:
            if not trail.node_explored(start_node):
                if self._bfs(trail, start_node, **self.callbacks(**kw)):
                    break
        return trail

    def _bfs(self, trail, start_node, enter_func, leave_func, backedge_func):
        trail.enqueue((start_node,None))
        trail.explore_node(start_node)
        while not trail.queue_empty():
            (dequeued_node, dequeued_edge) = trail.dequeue()
            trail.append_node(dequeued_node)
            if dequeued_edge is not None:
                trail.append_edge(dequeued_edge)
            stop = bool(enter_func(trail.graph, dequeued_node, dequeued_edge))
            stop |= bool(leave_func(trail.graph, dequeued_node, dequeued_edge))
            if stop:
                trail.result = dequeued_node
                return True
            for edge in self.select_edges(trail.graph, dequeued_node):
                adjacent_node = trail.graph.adjacent(dequeued_node, edge)
                if not trail.node_explored(adjacent_node):
                    trail.explore_edge(edge)
                    trail.explore_node(adjacent_node)
                    trail.enqueue((adjacent_node, edge))
                else:
                    if not trail.edge_explored(edge):
                        trail.explore_and_append_backedge(edge)
                        if backedge_func(trail.graph, edge):
                            trail.result = edge
                            return True
        return False

# vim: set ft=python et ts=4 sw=4:
