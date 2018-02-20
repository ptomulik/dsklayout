# -*- coding: utf8 -*-
"""Implements the @dispatch.on decorator

Implements the @dispatch.on decorator wich enables function overloading. The
function overloading via @dispatch.on resembles the corresponding feature of
C++ language, but is here far more limited. Function dispatching is based on a
signle argument only, the one pointed to by @dispatch.on decorator.

Usage example::

    from dsklayout.action import dispatch

    class A:
        def __repr__(self):
            return '<Object A>'
    class B:
        def __repr__(self):
            return '<Object B>'
    class C(A):
        def __repr__(self):
            return '<Object C>'

    @dispatch.on('x')
    def func(x):
        print("func(%s)" % repr(x))

    @func.when(A)
    def func(x):
        print("func<A>(%s)" % repr(x))

    @func.when(B)
    def func(x):
        print("func<B>(%s)" % repr(x))

    a = A()
    b = B()
    c = C()

    func(1) # -> "func(1)"
    func(a) # -> "func<A>(<Object A>)"
    func(b) # -> "func<B>(<Object B>)"
    func(c) # -> "func<A>(<Object C>)"
"""

import inspect
import collections
import functools

__all__ = ('dispatch',)


class _DispatchMeta(type):

    @property
    def dispatchers(cls):
        if not hasattr(cls, '_dispatchers'):
            cls._dispatchers = dict()
        return cls._dispatchers


class dispatch(object, metaclass=_DispatchMeta):

    __slots__ = ('_default', '_arg_index', '_arg_name', '_varargs', '_kwargs',
                 '_overloads')

    @classmethod
    def on(cls, arg_sel, **kw):
        """A decorator used to mark function as being overloaded"""
        def decorator(func):
            spec = inspect.getfullargspec(func)
            index, name = cls._handle_on_args(func, spec, arg_sel, **kw)
            instance = cls._get_instance(func, spec, index, name, **kw)

            @functools.wraps(func)
            def wrapper(*args, **kw):
                return instance(*args, **kw)

            wrapper.when = instance.when
            wrapper.on = cls.on
            wrapper.impl = instance  # for debugging/unit testing
            return wrapper
        return decorator

    @classmethod
    def _get_instance(cls, func, spec, arg_index, arg_name, **kw):
        name = cls._func_name(func)
        if name not in cls.dispatchers:
            cls.dispatchers[name] = cls(func, arg_index, arg_name, **kw)
        return cls.dispatchers[name]

    @classmethod
    def _func_name(cls, func):
        return '.'.join([func.__module__, func.__qualname__])

    @classmethod
    def _handle_on_args(cls, func, spec, arg_sel, **kw):
        arg_index, arg_name = cls._handle_arg_sel(func, spec, arg_sel, **kw)
        return (arg_index, arg_name)

    @classmethod
    def _handle_arg_sel(cls, func, spec, arg_sel, **kw):
        if isinstance(arg_sel, int):
            return cls._handle_int_arg_sel(func, spec, arg_sel, **kw)
        elif isinstance(arg_sel, str):
            return cls._handle_str_arg_sel(func, spec, arg_sel, **kw)
        else:
            raise TypeError(("%s.on() argument 1 must be either int " +
                             "or str, not %s") % (cls.__name__, repr(arg_sel)))

    @classmethod
    def _handle_int_arg_sel(cls, func, spec, arg_sel, **kw):
        arg_index = arg_sel
        n = len(spec.args)
        if arg_index < 0:
            raise ValueError("negative argument index: %s" % repr(arg_index))
        elif arg_index >= n:
            if spec.varargs is None:
                raise ValueError(("%s() takes %s positional arguments " +
                                  "(indices 0 through %s), but argument " +
                                  "index %s was selected for dispatching") %
                                 (func.__name__, repr(n), repr(n-1),
                                  arg_index))
            elif not kw.get('varargs'):
                raise ValueError(("%s() takes %s positional arguments " +
                                  "(indices 0 through %s) and variadic " +
                                  "arguments (unused by %s), however, " +
                                  "argument index %s was selected for " +
                                  "dispatching") %
                                 (func.__name__, repr(n), repr(n-1),
                                  cls.__name__, arg_index))
            else:
                arg_name = None
        else:
            arg_name = spec.args[arg_index]

        return (arg_index, arg_name)

    @classmethod
    def _handle_str_arg_sel(cls, func, spec, arg_sel, **kw):
        if arg_sel in spec.args:
            arg_index = spec.args.index(arg_sel)
        elif spec.varkw is None:
            raise ValueError(("%s() has no positional argument named %s " +
                              "and takes no keyword arguments") %
                             (func.__name__, repr(arg_sel)))
        elif not kw.get('kwargs'):
            raise ValueError(("%s() has no positional argument named %s " +
                              "and keyword arguments are disabled") %
                             (func.__name__, repr(arg_sel)))
        else:
            arg_index = None
        arg_name = arg_sel
        return (arg_index, arg_name)

    @classmethod
    def _handle_func(cls, func, spec, arg_index, arg_name):
        if arg_index is not None:
            cls._handle_func_arg_index(func, spec, arg_index)
        elif arg_name is not None:
            cls._handle_func_arg_name(func, spec, arg_name)
        else:
            raise RuntimeError("bug: both arg_index and arg_name are None")

    @classmethod
    def _handle_func_arg_index(cls, func, spec, arg_index):
        n = len(spec.args)
        if arg_index < 0:
            raise RuntimeError("bug: negative arg_index: %r" % arg_index)
        elif n <= arg_index and spec.varargs is None:
            if n > 1:
                takes = ("only %r positional arguments (indices 0 " +
                         "through %r)") % (n, n-1)
            elif n == 1:
                takes = "only 1 positional argument (index 0)"
            else:
                takes = "no positional arguments"
            raise TypeError(("argument index %s was selected for " +
                             "dispatching, but %s() takes %s") %
                            (arg_index, func.__name__, takes))

    @classmethod
    def _handle_func_arg_name(cls, func, spec, arg_name):
        if arg_name not in spec.args and spec.varkw is None:
            raise TypeError(("argument named %s was selected for " +
                             "dispatching, but %s() has no positional " +
                             "argument named %s and takes no keyword " +
                             "arguments") %
                            (repr(arg_name), func.__name__, repr(arg_name)))

    def __init__(self, func, arg_index, arg_name, **kw):
        self._default = func
        self._overloads = dict()
        self._arg_index = arg_index
        self._arg_name = arg_name
        self._kwargs = kw.get('kwargs')
        self._varargs = kw.get('varargs')

    def __call__(self, *args, **kw):
        klass = self._getclass(args, kw)
        if klass is not None:
            return self._lookup(klass)(*args, **kw)
        else:
            return self._default(*args, **kw)

    def _getclass(self, args, kw):
        """Returns class of dispatching argument (one of args or kw)"""
        if self._arg_index is not None:
            if self._arg_index < len(args):
                return args[self._arg_index].__class__
            elif self._varargs:
                return None
            else:
                n = 1 + self._arg_index - len(args)
                s = "argument" if n == 1 else "arguments"
                raise TypeError("%s() missing %s required positional %s" %
                                (self._default.__name__, n, s))
        else:
            return kw.get(self._arg_name).__class__

    def _lookup(self, klass):
        """Find first function which can accept an instance of klass as its
           dispatching argument"""
        queue = collections.deque()
        queue.append(klass)
        while queue:
            dc = queue.popleft()
            try:
                return self._overloads[dc]
            except KeyError:
                pass
            for base in dc.__bases__:
                queue.append(base)
        return self._default  # default function to be called

    def when(self, klass):
        """A decorator used to declare an overloaded version of function"""
        def decorator(func):
            spec = inspect.getfullargspec(func)
            self._handle_when_args(func, spec, klass)
            self._overloads[klass] = func

            @functools.wraps(func)
            def wrapper(*args, **kw):
                return self(*args, **kw)

            wrapper.when = self.when
            wrapper.on = self.__class__.on
            wrapper.impl = self  # for debugging/unit testing
            return wrapper
        return decorator

    def _handle_when_args(self, func, spec, klass):
        if not inspect.isclass(klass):
            raise TypeError(("%s.when() argument 1 must be a type, not %s") %
                            (self.__class__.__name__, repr(klass)))
        self._handle_func(func, spec, self._arg_index, self._arg_name)


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
