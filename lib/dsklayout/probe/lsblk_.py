# -*- coding: utf8 -*-

from . import backtick_
from .. import util
from ..device import Device
from ..graph import Graph

import json

__all__ = ('LsBlkProbe', 'PropertyError')


class PropertyError(Exception):
    pass


class _GraphBuilder:
    """Bulids graph from LsBlkProbe nodes. It's intended to be used as function
       in LsBlkProbe._apply_recursive"""

    __slots__ = ('_graph', '_keyattr')

    def __init__(self, **kw):
        self._graph = Graph(**kw)
        self._keyattr = kw.get('keyattr', 'kname')

    @property
    def graph(self):
        return self._graph

    @property
    def keyattr(self):
        return self._keyattr

    def __call__(self, node, parent=None):
        key = node[self.keyattr]
        props = {k:  v for (k, v) in node.items() if k != 'children'}
        if not self.graph.has_node(key):
            self.graph.add_node(key, Device(_Properties.new(props).properties))
        else:
            _Properties(self.graph.node(key).properties).update(props)
        if parent is not None:
            self.graph.add_edge((parent[self.keyattr], key))


class _Properties:

    __slots__ = ('_properties', '_convert')

    # values of these properties get collected from multiple lsblk nodes
    _collective = ('pkname',)

    # how we can convert values obtained from lsblk
    _converters = {
            'parttype': lambda x: int(x, 16),  # hex str to int
            'ra': int,
            'ro': lambda x: bool(int(x)),
            'rm': lambda x: bool(int(x)),
            'hotplug': lambda x: bool(int(x)),
            'alignment': int,
            'min-io': int,
            'opt-io': int,
            'phy-sec': int,
            'log-sec': int,
            'rota': lambda x: bool(int(x)),
            'rq-size': int,
            'rand': lambda x: bool(int(x)),
    }

    def __init__(self, initial=None, **kw):
        self._properties = initial or dict()
        self._convert = kw.get('convert', False)

    @classmethod
    def new(cls, properties=(), **kw):
        return cls(**kw).set(properties)

    @property
    def properties(self):
        return self._properties

    def set(self, properties):
        """Called when node properties appear for the first time"""
        self._properties = self._convert_if_enabled(properties)
        self._for_collective_props(self._assign_collective_prop, properties)
        return self

    def update(self, properties):
        """Called when node properties appear again"""
        properties = self._convert_if_enabled(properties)

        # first verify input
        for key in (set(properties) - set(self._collective)):
            if self.properties.get(key) == properties[key]:
                continue
            msg = "Conflicting values for property %s: %s vs %s" % \
                  (key, repr(self.properties.get(key)), repr(properties[key]))
            raise PropertyError(msg)

        # then update collective properties
        self._for_collective_props(self._update_collective_prop, properties)
        return self

    def _convert_if_enabled(self, properties):
        if self._convert:
            return self._convert_values(properties)
        else:
            return dict(properties)

    def _for_collective_props(self, func, properties):
        for key in (set(self._collective) & set(properties)):
            func(key, properties[key])

    def _assign_collective_prop(self, key, value):
        if value is None:
            self.properties[key] = []
        else:
            self.properties[key] = [value]

    def _update_collective_prop(self, key, value):
        if key not in self.properties:
            self.properties[key] = []
        if value is not None and value not in self.properties[key]:
            self.properties[key].append(value)

    @classmethod
    def _convert_value(cls, key, value):
        if value is not None:
            return (cls._converters.get(key, lambda x:  x))(value)
        return None

    @classmethod
    def _convert_values(cls, items):
        if hasattr(items, 'items'):
            items = items.items()
        return {k:  cls._convert_value(k, v) for k, v in items}


class LsBlkProbe(backtick_.BackTickProbe):

    @classmethod
    def command(cls, **kw):
        return kw.get('lsblk', 'lsblk')

    @classmethod
    def flags(cls, flags, **kw):
        return ['-J', '-O', '-p'] + flags

    @classmethod
    def parse(cls, output):
        return json.loads(output)

    def graph(self, **kw):
        """Builds and returns graph with nodes representing block devices"""
        return self._apply_recursive(_GraphBuilder(**kw)).graph

    def spec(self):
        return self

    def _apply_recursive(self, func):
        nodes = self._content['blockdevices']
        LsBlkProbe._apply_recursive_to(func, nodes)
        return func

    @staticmethod
    def _apply_recursive_to(func, nodes, parent=None):
        for node in nodes:
            func(node, parent)
            children = node.get('children', [])
            LsBlkProbe._apply_recursive_to(func, children, node)


# vim: set ft=python et ts=4 sw=4:
