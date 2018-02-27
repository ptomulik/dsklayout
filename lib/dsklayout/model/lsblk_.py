# -*- coding: utf8 -*-

from . import lsblkdev_
from . import backtick_
from ..graph import Graph

import json

__all__ = ('LsBlk',)


class LsBlk(backtick_.BackTick):

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
        graph = Graph(**kw)
        for device in self._content['blockdevices']:
            self._graph_add_recursive(graph, device, **kw)
        return graph

    def _graph_add_recursive(self, graph, device, parent=None, **kw):
        self._graph_add(graph, device, parent, **kw)
        for child in device.get('children', []):
            self._graph_add_recursive(graph, child, device, **kw)

    def _graph_add(self, graph, device, parent=None, **kw):
        keyattr = kw.get('keyattr', 'kname')
        key = device[keyattr]
        props = {k:  v for (k, v) in device.items() if k != 'children'}
        if not graph.has_node(key):
            graph.add_node(key, lsblkdev_.LsBlkDev(props))
        else:
            graph.node(key).reappear(props)
        if parent is not None:
            graph.add_edge((parent[keyattr], key))


# vim: set ft=python et ts=4 sw=4:
