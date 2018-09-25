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


def _dump_other_object(obj):
    return _dump_or_load_other_object(obj, dump_object)


def _load_other_object(data):
    return _dump_or_load_other_object(data, load_object)


def _dump_or_load_other_object(subj, func):
    if isinstance(subj, dict):
        return {k: func(v) for k, v in subj.items()}
    elif isinstance(subj, list):
        return [func(v) for v in subj]
    else:
        return subj


# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
