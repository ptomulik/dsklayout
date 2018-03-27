# -*- coding: utf8 -*-

import collections.abc
import json
from .. import util

__all__ = ('Elems',)


class _missing_meta(type):
    "Meta-class for the `_missing` class"

    def __bool__(self):
        return False
    __nonzero__ = __bool__

    def __repr__(cls):
        return 'MISSING'


class _missing(object, metaclass=_missing_meta):
    "Represents missing argument to function."
    pass

MISSING = _missing
"""Represents missing argument to a function."""


class Elems(collections.abc.MutableMapping):
    """A container for graph elements, either edges or nodes.
    """

    __slots__ = ('_data',)

    def __init__(self, items=(), **kw):
        super().__init__()
        self._data = dict()
        self.update(items, **kw)

    @property
    def data(self):
        """A {node: value} dictionary, with custom values"""
        return self._data

    def __contains__(self, key):
        return key in self._data

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        if self._data:
            return "%s(%s)" % (self.__class__.__name__, repr(self._data))
        else:
            return "%s()" % self.__class__.__name__

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, data):
        return self.add(key, data)

    def __delitem__(self, key):
        del self._data[key]

    def add(self, key, data=MISSING):
        if data is MISSING:
            if key not in self._data:
                self._data[key] = None
        else:
            self._data[key] = data

    def discard(self, key):
        if key in self:
            del self[key]

    def clear(self):
        self._data.clear()

    def items(self):
        return self._data.items()

    def update(self, items, **kw):
        has_items = hasattr(items, 'items')
        if has_items:
            items = items.items()
        if kw.get('data', has_items):
            self._update_with_values(items)
        else:
            self._update_without_values(items)

    def dump_attributes(self):
        return {'items': [(k, util.dump_object(v)) for k, v in self.data.items()]}

    @classmethod
    def load_attributes(cls, attributes):
        items = [(k, util.load_object(v)) for k, v in attributes['items']]
        return cls(items, data=True)

    def _update_with_values(self, items):
        for e, d in items:
            self.add(e, d)

    def _update_without_values(self, items):
        for e in items:
            self.add(e)

# vim: set ft=python et ts=4 sw=4:
