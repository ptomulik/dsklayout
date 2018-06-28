# -*- coding: utf8 -*-

import abc

__all__ = ('Probe',)


class Probe(object, metaclass=abc.ABCMeta):
    """Encapsulates data obtained from a predefined external program."""

    __slots__ = ('_content',)

    def __init__(self, content):
        """Initializes the Probe."""
        self._content = content

    @property
    def content(self):
        """Data encapsulated by this object"""
        return self._content

    def dump_attributes(self):
        return {'content': self.content}

    @classmethod
    def load_attributes(cls, attributes):
        return cls(attributes['content'])



# vim: set ft=python et ts=4 sw=4:
