# -*- coding: utf8 -*-

from . import trail_

import collections
import abc

__all__ = ( 'Traversal', )

class Traversal(object, metaclass=abc.ABCMeta):
    """An abstract base class for graph traversal (search) algorithms"""

    __slots__ = ( '_edge_selector',
                  '_enter_func',
                  '_leave_func',
                  '_backedge_func' )

    def __init__(self, **kw):
        self.edge_selector = kw.get('edge_selector')
        self.enter_func = kw.get('enter_func', lambda g, n, e: False)
        self.leave_func = kw.get('leave_func', lambda g, n, e: False)
        self.backedge_func = kw.get('backedge_func', lambda g,e: False)

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
    def enter_func(self):
        """Callback function invoked when Traverser enters a node."""
        return self._enter_func

    @enter_func.setter
    def enter_func(self, func):
        if not callable(func):
            raise TypeError("enter_func must be callable, %s provided" % func.__class__.__name__)
        self._enter_func = func

    @property
    def leave_func(self):
        """Callback function invoked when Traverser leaves a node."""
        return self._leave_func

    @leave_func.setter
    def leave_func(self, func):
        if not callable(func):
            raise TypeError("leave_func must be callable, %s provided" % func.__class__.__name__)
        self._leave_func = func

    @property
    def backedge_func(self):
        """Callback function invoked when Traverser spots a back edge."""
        return self._backedge_func

    @backedge_func.setter
    def backedge_func(self, func):
        if not callable(func):
            raise TypeError("backedge_func must be callable, %s provided" % func.__class__.__name__)
        self._backedge_func = func

    @property
    def default_edge_selector(self):
        return self.select_incident_edges

    def select_edges(self, graph, node):
        """Select edges to be tried next"""
        return (self.edge_selector)(graph, node)

    def select_incident_edges(self, graph, node):
        """Returns edges incident to given node"""
        return graph.incident(node)

    def select_inward_edges(self, graph, node):
        """Returns edges inward to given node"""
        return graph.inward(node)

    def select_outward_edges(self, graph, node):
        """Returns edges outward to given node"""
        return graph.outward(node)

    def callbacks(self, **kw):
        """Returns a dictionary of callbacks from kw, defaulting to callbacks defined by object"""
        callbacks = ( 'enter_func', 'leave_func', 'backedge_func' )
        return { k : kw.get(k, getattr(self,k)) for k in callbacks }

    @abc.abstractmethod
    def __call__(self, graph, startpoint, *args, **kw):
        pass

# vim: set ft=python et ts=4 sw=4:
