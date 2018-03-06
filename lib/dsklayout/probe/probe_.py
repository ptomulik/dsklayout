# -*- coding: utf8 -*-

import abc

__all__ = ('Probe',)


class Probe(object, metaclass=abc.ABCMeta):

    __slots__ = ('_content',)

    def __init__(self, content):
        self._content = content

    @property
    def content(self):
        return self._content



# vim: set ft=python et ts=4 sw=4:
