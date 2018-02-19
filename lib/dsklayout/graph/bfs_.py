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
        trail = trail_.Trail(graph, **self.callbacks(**kw))
        for start_node in start_nodes:
            if trail.node_explored(start_node):
                continue
            if self._bfs(trail, start_node):
                break
        return trail

    def _bfs(self, trail, start_node):
        trail.enqueue((start_node,None))
        trail.explore_node(start_node)
        while not trail.queue_empty():
            (node, edge) = trail.dequeue()
            if self._handle_dequeued(trail, node, edge):
                return True
            if self._enqueue_adjacent_nodes(trail, node):
                return True
        return False

    def _handle_dequeued(self, trail, node, edge):
        trail.append_node(node)
        if edge is not None:
            trail.append_edge(edge)
        stop = bool(trail.ingress_func(trail.graph, node, edge))
        stop |= bool(trail.egress_func(trail.graph, node, edge))
        if stop:
            trail.result = node
        return stop

    def _enqueue_adjacent_nodes(self, trail, node):
        for edge in self.select_edges(trail.graph, node):
            adjacent_node = trail.graph.adjacent(node, edge)
            if self._handle_adjacent_node(trail, adjacent_node, edge):
                return True
        return False

    def _handle_adjacent_node(self, trail, node, edge):
        if not trail.node_explored(node):
            trail.explore_edge(edge)
            trail.explore_node(node)
            trail.enqueue((node, edge))
            return False
        else:
            return self._handle_backedge(trail, edge)

    def _handle_backedge(self, trail, edge):
        if not trail.edge_explored(edge):
            trail.explore_and_append_backedge(edge)
            if trail.backedge_func(trail.graph, edge):
                trail.result = edge
                return True
        return False

# vim: set ft=python et ts=4 sw=4:
