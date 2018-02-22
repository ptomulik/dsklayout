# -*- coding: utf8 -*-
"""Utility functions to automate (sub)module imports.
"""

import importlib
import inspect
import sys

__all__ = ('import_all_from', 'import_from')


def import_all_from(target, modules, module_package=None, **kw):
    """Imports symbols from multiple modules.

       For each module in modules, this is an equivalent of:

            from module import *
            __all__ += module.__all__
    """
    if isinstance(modules, str) or inspect.ismodule(modules):
        modules = (modules,)
    if isinstance(target, str):
        target_module = sys.modules[target]
    else:
        target_module = target
        target = target.__name__
    for module in modules:
        if isinstance(module, str):
            module = importlib.import_module(module, module_package or target)
        import_from(target_module, module, all_symbols(module), **kw)


def import_from(target, source, symbols, **kw):
    for symbol in symbols:
        setattr(target, symbol, getattr(source, symbol))
    if kw.get('__all__', True):
        if not hasattr(target, '__all__'):
            target.__all__ = ()
        target.__all__ += target.__all__.__class__(symbols)


def all_symbols(module):
    if hasattr(module, '__all__'):
        return module.__all__
    else:
        return dir(module)


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
