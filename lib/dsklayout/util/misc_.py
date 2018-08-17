# -*- coding: utf8 -*-
"""Miscellaneous utilities
"""

__all__ = ('add_dict_getters',)


def add_dict_getters(cls, mappings, dict):
    """Add property getters to a class. The properties are assumed to be kept
    in an internal dictionary."""
    for attr, key in mappings.items():
        setattr(cls, attr, property(lambda o, k=key: getattr(o, dict).get(k)))


# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
