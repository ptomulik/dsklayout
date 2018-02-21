# -*- coding: utf8 -*-

import importlib
import sys

def inject_symbols_from_modules(target, modules, module_package=None, **kw):
    """Imports symbols from multiple modules. See inject_symbols_from_module"""
    for module in modules:
        inject_symbols_from_module(target, module, module_package, **kw)


def inject_symbols_from_module(target, module, package=None, **kw):
    """Imports all symbols from module to target.

    An equivalent of:

        from module import *
        __all__ += module.__all__
    """
    target_module = sys.modules[target]
    module = importlib.import_module(module, package or target)
    inject_symbols(target_module, module, exportable_symbols(module), **kw)


def inject_symbols(target, source, symbols, **kw):
    for symbol in symbols:
        setattr(target, symbol, getattr(source, symbol))
    if kw.get('__all__', True):
        if not hasattr(target, '__all__'):
            target.__all__ = ()
        target.__all__ += target.__all__.__class__(symbols)


def exportable_symbols(module):
    if hasattr(module, '__all__'):
        return module.__all__
    else:
        return dir(module)

inject_symbols_from_modules(__package__, [
        '.dispatch_',
        '.subprocess_'
    ])

# vim: set ft=python et ts=4 sw=4:
