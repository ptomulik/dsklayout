# -*- coding: utf8 -*-

from . import backtick_
from .. import util
from ..model import LsBlkDev
from ..graph import Graph

import json

__all__ = ('LsBlkProbe',)


class _GraphBuilder(object):
    """Bulids graph from LsBlkProbe nodes. It's intended to be used as function
       in LsBlkProbe._apply_recursive"""

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
            self.graph.add_node(key, LsBlkDev(props))
        else:
            self.graph.node(key).reappear(props)
        if parent is not None:
            self.graph.add_edge((parent[self.keyattr], key))


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
