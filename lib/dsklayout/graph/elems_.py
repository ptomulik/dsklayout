# -*- coding: utf8 -*-

import collections.abc

__all__ = ( 'Elems', )

class _missing:
    """Represents missing argument to function"""
    pass

class Elems(collections.abc.MutableMapping):
    """A container for graph elements, either edges or nodes.
    """

    __slots__ = ( '_data',  )

    def __init__(self, items = (), **kw):
        super().__init__()
        self._data = dict()
        if hasattr(items, 'items'):
            items = items.items()
            data = kw.get('data', True)
        else:
            data = kw.get('data', False)
        if data:
            for e,d in items: self.add(e,d)
        else:
            for e in items: self.add(e)

    @property
    def data(self):
        """Returns a dictionary which maps graph elements onto assigned data objects"""
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

    def add(self, key, data=_missing):
        if data is _missing:
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

# vim: set ft=python et ts=4 sw=4:
