# -*- coding: utf8 -*-
"""Serialization API for dsklayout
"""

import importlib

__all__ = ('dump_object', 'load_object')

def dump_object(obj):
    if hasattr(obj, 'dump_attributes'):
        return _dump_object_with_attributes(obj)
    else:
        return _dump_other_object(obj)

def load_object(data):
    obj = _load_object_with_attributes(data)
    if obj is None:
        obj = _load_other_object(data)
    return obj

def _dump_other_object(obj):
    if isinstance(obj, dict):
        return {k: dump_object(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [dump_object(v) for v in obj]
    else:
        return obj


def _dump_object_with_attributes(obj):
    cls = obj.__class__
    return {'_module': cls.__module__,
            '_class': cls.__name__,
            '_attributes': obj.dump_attributes()}

def _load_object_with_attributes(data):
    try:
        modname = data['_module']
        clsname = data['_class']
        attribs = data['_attributes']
    except (TypeError, KeyError):
        return None
    else:
        mod = importlib.import_module(modname)
        cls = getattr(mod, clsname)
        if hasattr(cls, 'load_attributes'):
            return cls.load_attributes(attribs)
        else:
            return cls(**attribs)

def _load_other_object(data):
    if isinstance(data, dict):
        return {k: load_object(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [load_object(v) for v in data]
    else:
        return data

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
