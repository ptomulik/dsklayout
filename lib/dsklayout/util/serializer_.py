# -*- coding: utf8 -*-
"""Serializer
"""

import importlib

__all__ = ('dump_object', 'load_object')


def dump_object(obj):
    if hasattr(obj, 'dump_attributes'):
        cls = obj.__class__
        return {'_module': cls.__module__,
                '_class': cls.__name__,
                '_attributes': obj.dump_attributes()}
    else:
        return obj

def load_object(data):
    try:
        modname = data['_module']
        clsname = data['_class']
        attribs = data['_attributes']
    except (TypeError, KeyError):
        return data
    else:
        mod = importlib.import_module(modname)
        cls = getattr(mod, clsname)
        if hasattr(cls, 'load_attributes'):
            return cls.load_attributes(attribs)
        else:
            return cls(**attribs)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
