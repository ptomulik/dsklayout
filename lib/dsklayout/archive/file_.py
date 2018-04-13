# -*- coding: utf8 -*-

from .. import util

__all__ = ('ArchiveFile',)


class ArchiveFile:

    __slots__ = ('_path', '_meta')

    def __init__(self, path, _meta=None):
        self._path = path
        self._meta = meta

    @property
    def path(self):
        return self._path

    @property
    def meta(self):
        return self._meta




# vim: set ft=python et ts=4 sw=4:
