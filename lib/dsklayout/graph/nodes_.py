# -*- coding: utf8 -*-

from . import elems_

import collections.abc

__all__ = ( 'Nodes', )

class Nodes(elems_.Elems):
    """An unordered set of graph nodes with data items optionally attached."""

    def __init__(self, items = (), **kw):
        if 'nodedata' in kw: kw['data'] = kw['nodedata']
        super().__init__(items, **kw)

# vim: set ft=python et ts=4 sw=4:
