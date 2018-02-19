# -*- coding: utf8 -*-

import collections

__all__ = ('Trail',)


class Trail(object):

    def __init__(self, graph, **kw):
        self._graph = graph
        self._explored_nodes = set()
        self._explored_edges = set()
        self._nodes = list()
        self._edges = list()
        self._backedges = list()
        self._result = None
        self._queue = collections.deque()
        self._ingress_func = kw.get('ingress_func', lambda *args:  False)
        self._egress_func = kw.get('egress_func', lambda *args:  False)
        self._backedge_func = kw.get('backedge_func', lambda *args:  False)

    @property
    def explored_nodes(self):
        """A set of already explored nodes"""
        return self._explored_nodes

    @property
    def explored_edges(self):
        """A set of already explored edges"""
        return self._explored_edges

    @property
    def nodes(self):
        """A list of nodes found by traversal algorithm (in original order)"""
        return self._nodes

    @property
    def edges(self):
        """A list of already traversed edges"""
        return self._edges

    @property
    def backedges(self):
        """A list of back edges (skipped due to cycles)"""
        return self._backedges

    @property
    def queue(self):
        """A node queue used, for example, by BFS algorithm"""
        return self._queue

    @property
    def result(self):
        """A result saved by a search algorithm"""
        return self._result

    @result.setter
    def result(self, result):
        self._result = result

    @property
    def graph(self):
        """A graph provided as the argument to __init__()"""
        return self._graph

    @property
    def ingress_func(self):
        """A callback invoked when a search algorithm enters a node"""
        return self._ingress_func

    @property
    def egress_func(self):
        """A callback invoked when a search algorithm leaves a node"""
        return self._egress_func

    @property
    def backedge_func(self):
        """A callback invoked when a search algorithm finds a backedges"""
        return self._backedge_func

    def node_explored(self, node):
        """Returns whether a node was already explored"""
        return node in self._explored_nodes

    def edge_explored(self, edge):
        """Returns whether an edge was already explored"""
        return edge in self._explored_edges

    def explore_node(self, node):
        """Add node to the set of explored nodes"""
        self._explored_nodes.add(node)

    def explore_edge(self, edge):
        """Add edge to the set of explored edges"""
        self._explored_edges.add(edge)

    def append_node(self, node):
        """Append node to the list of visited nodes"""
        self._nodes.append(node)

    def append_edge(self, edge):
        """Append edge to the list of visited edges"""
        self._edges.append(edge)

    def append_backedge(self, backedge):
        """Append backedge to the list of visited backedges"""
        self._backedges.append(backedge)

    def explore_and_append_node(self, node):
        """Append node to self.nodes and add to self.explored_nodes"""
        self.explore_node(node)
        self.append_node(node)

    def explore_and_append_edge(self, edge):
        """Append edge to self.edges and add to self.explored_edges"""
        self.explore_edge(edge)
        self.append_edge(edge)

    def explore_and_append_backedge(self, edge):
        """Append edge to self.backedges and add to self.explored_edges"""
        self.explore_edge(edge)
        self.append_backedge(edge)

    def enqueue(self, node):
        """Enqueue node in self.queue"""
        self._queue.append(node)

    def dequeue(self):
        """Dequeue first node from self.queue"""
        return self._queue.popleft()

    def queue_empty(self):
        """Returns True iff self.queue is empty"""
        return not self._queue

# vim: set ft=python et ts=4 sw=4:
