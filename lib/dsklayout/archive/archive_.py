# -*- coding: utf8 -*-

from .. import util

__all__ = ('Archive',)


class Archive:

    __slots__ = ('_graph', '_attachments', '_file')

    def __init__(self, graph=None, **kw):
        self._graph = graph
        self._attachments = attachments or dict()

    @property
    def graph(self):
        return self._graph

    @property
    def attachments(self):
        return self._attachments

    def attach(self, attachment, key=None):
        self.attachments[(key or attachment.key)] = attachment

    def dump_attributes(self):
        return {'graph': util.dump_object(self.graph),
                'attachments': util.dump_object(self.attachments)}

    @classmethod
    def load_attributes(cls, attributes):
        kw = {'graph': util.load_object(attributes['graph']),
              'attachments': util.load_object(attributes['attachments'])}
        return cls(**kw)



# vim: set ft=python et ts=4 sw=4:
