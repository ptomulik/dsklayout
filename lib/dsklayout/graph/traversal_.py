# -*- coding: utf8 -*-

from . import trail_

import collections
import abc

__all__ = ('Traversal',)


class Traversal(object, metaclass=abc.ABCMeta):
    """An abstract base class for graph traversal (search) algorithms"""

    __slots__ = ('_edge_selector',
                 '_ingress_func',
                 '_egress_func',
                 '_backedge_func')

    def __init__(self, **kw):
        self.edge_selector = kw.get('edge_selector', kw.get('direction'))
        self.ingress_func = kw.get('ingress_func', lambda g, n, e: False)
        self.egress_func = kw.get('egress_func', lambda g, n, e: False)
        self.backedge_func = kw.get('backedge_func', lambda g, e: False)

    @property
    def edge_selector(self):
        return self._edge_selector

    @edge_selector.setter
    def edge_selector(self, selector):
        if selector is None:
            self._edge_selector = self.default_edge_selector
        elif callable(selector):
            self._edge_selector = selector
        elif hasattr(self, 'select_%s_edges' % selector):
            self._edge_selector = getattr(self, 'select_%s_edges' % selector)
        else:
            raise ValueError('Invalid edge selector %s' % repr(selector))

    @property
    def ingress_func(self):
        """Callback function invoked when Traverser enters a node."""
        return self._ingress_func

    @ingress_func.setter
    def ingress_func(self, func):
        if not callable(func):
            raise TypeError("ingress_func must be callable, %s provided" %
                            func.__class__.__name__)
        self._ingress_func = func

    @property
    def egress_func(self):
        """Callback function invoked when Traverser leaves a node."""
        return self._egress_func

    @egress_func.setter
    def egress_func(self, func):
        if not callable(func):
            raise TypeError("egress_func must be callable, %s provided" %
                            func.__class__.__name__)
        self._egress_func = func

    @property
    def backedge_func(self):
        """Callback function invoked when Traverser spots a back edge."""
        return self._backedge_func

    @backedge_func.setter
    def backedge_func(self, func):
        if not callable(func):
            raise TypeError("backedge_func must be callable, %s provided" %
                            func.__class__.__name__)
        self._backedge_func = func

    @property
    def default_edge_selector(self):
        return self.select_incident_edges

    def select_edges(self, graph, node):
        """Select edges to be tried next"""
        return (self.edge_selector)(graph, node)

    def select_inward_edges(self, graph, node):
        """Returns edges inward to given node"""
        return graph.inward(node)

    def select_incident_edges(self, graph, node):
        """Returns edges incident to given node"""
        return graph.incident(node)

    def select_both_edges(self, graph, node):
        """Returns edges incident to given node"""
        return graph.incident(node)

    def select_outward_edges(self, graph, node):
        """Returns edges outward to given node"""
        return graph.outward(node)

    def callbacks(self, **kw):
        """Extracts and returns callbacks from keyword arguments"""
        callbacks = ('ingress_func', 'egress_func', 'backedge_func')
        return {k: kw.get(k, getattr(self, k)) for k in callbacks}

    @abc.abstractmethod
    def __call__(self, graph, startpoint, *args, **kw):
        pass

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
