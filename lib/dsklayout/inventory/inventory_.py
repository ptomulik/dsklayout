# -*- coding: utf8 -*-

from .. import util

__all__ = ('Inventory',)


class Inventory:

    __slots__ = ('_graph',)

    def __init__(self, graph=None):
        self._graph = graph

    @property
    def graph(self):
        return self._graph

    def dump_attributes(self):
        return {'graph': util.dump_object(self.graph)}

    @classmethod
    def load_attributes(cls, attributes):
        graph = util.load_object(attributes['graph'])
        return cls(graph)



# vim: set ft=python et ts=4 sw=4:
