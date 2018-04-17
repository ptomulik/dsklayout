# -*- coding: utf8 -*-

from .. import util

__all__ = ('ArchiveFile',)


class ArchiveFile:

    __slots__ = ('_path', '_meta')

    def __init__(self, path, meta=None):
        self._path = path
        self._meta = meta or dict()

    @property
    def path(self):
        return self._path

    @property
    def meta(self):
        return self._meta

    def dump_attributes(self):
        return {'path': self.path, 'meta': self.meta}

    @classmethod
    def load_attributes(cls, attributes):
        kw = {'path': attributes['path'], 'meta': attributes['meta']}
        return cls(**kw)




# vim: set ft=python et ts=4 sw=4:
