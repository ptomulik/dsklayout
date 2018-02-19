# -*- coding: utf8 -*-

from . import blkdev_
from ..util import backtick
from ..graph import Graph

import json

__all__ = ('LsBlk',)


class LsBlk(object):

    __slots__ = ('_content',)

    def __init__(self, content):
        self._content = content

    @property
    def content(self):
        return self._content

    def _graph_add(self, graph, device, parent=None, **kw):
        keyattr = kw.get('keyattr', 'kname')
        key = device[keyattr]
        props = {k:  v for (k, v) in device.items() if k != 'children'}
        if not graph.has_node(key):
            graph.add_node(key, blkdev_.BlkDev(props))
        else:
            graph.node(key).reappear(props)
        if parent is not None:
            graph.add_edge((parent[keyattr], key))

    def _graph_add_walk(self, graph, device, parent=None, **kw):
        self._graph_add(graph, device, parent, **kw)
        for child in device.get('children', []):
            self._graph_add_walk(graph, child, device, **kw)

    def graph(self, **kw):
        """Builds and returns graph with nodes representing block devices"""
        graph = Graph(**kw)
        for device in self._content['blockdevices']:
            self._graph_add_walk(graph, device, **kw)
        return graph

    @staticmethod
    def run(devices=None, flags=None, **kw):
        """Runs lsblk(8) program for specified devices and returns its output.

        If ``devices`` is missing (or None), the program will be invoked
        without device arguments. The program is ran with -J, -O, -p flags
        (json output with all fields and full device paths instead of short
        names). Additional flags may be provided via ``flags`` parameter.
        """
        if devices is None:
            devices = []
        elif isinstance(devices, str):
            devices = [devices]
        if flags is None:
            flags = []
        lsblk = kw.get('lsblk', 'lsblk')
        return backtick([lsblk, '-J', '-O', '-p'] + flags + devices)

    @staticmethod
    def new(devices=None, flags=None, **kw):
        """Creates a new instance of LsBlk for specified devices by running and
           interpreting the output of lsblk(8) program."""
        output = LsBlk.run(devices, flags, **kw)
        content = json.loads(output)
        return LsBlk(content)

# vim: set ft=python et ts=4 sw=4:
