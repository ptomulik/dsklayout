# -*- coding: utf8 -*-

from .. import util
import copy

__all__ = ('ArchiveMetadata',)

class ArchiveMetadata:

    __slots__ = ('_graph', '_files')

    def __init__(self, graph=None, files=None):
        self._graph = graph
        self._files = files or dict()

    def copy(self):
        return copy.deepcopy(self)

    @property
    def graph(self):
        return self._graph

    @property
    def files(self):
        return self._files

    def dump_attributes(self):
        return {'graph': util.dump_object(self.graph),
                'files': util.dump_object(self.files)}

    @classmethod
    def load_attributes(cls, attributes):
        kw = {'graph': util.load_object(attributes['graph']),
              'files': util.load_object(attributes['files'])}
        return cls(**kw)


# vim: set ft=python et ts=4 sw=4:
