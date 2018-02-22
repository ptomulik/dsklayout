# -*- coding: utf8 -*-
"""Provides the Factory class
"""

import sys
import inspect
import abc

__all__ = ('Factory', 'FactoryError', 'FactorySubject')


class FactoryError(Exception):
    pass


class FactorySubject(object, metaclass=abc.ABCMeta):

    @classmethod
    @abc.abstractmethod
    def supports(cls, spec):
        """Shall return positive integer, if cls(cls.adjust(spec)) is supposed
           to return valid object. Otherwise, should return a value which
           evaluates to False in boolean context.

           Classes, which declare to support given spec, get sorted by
           cls.supports(spec) in descending order and a class with highest
           score is selected by factory.produce(spec) to create an instance.
        """
        pass

    @classmethod
    def adjust(cls, spec):
        """Adjusts spec such that it's useful as constructor's argument."""
        return spec


class Factory(object):
    """Given a base class and an abstract specification of an instance, it
    selects a subclass which best matches specification and creates an instance
    of this subclass. The specification matching is delegated to subclasses
    of FactorySubject."""

    @classmethod
    def factories(cls):
        """Dictionary which maps product base classes to factory objects"""
        if not hasattr(cls, '_factories'):
            cls._factories = dict()
        return cls._factories

    @classmethod
    def factory(cls, base, **kw):
        if not issubclass(base, FactorySubject):
            raise TypeError("%s is not supported by Factory.factory()" % \
                            type(base).__name__)
        factories = cls.factories()
        if base not in factories:
            factories[base] = cls(base, **kw)
        return factories[base]

    def __init__(self, base, **kw):
        self._base = base
        self._classes = self._find_classes(**kw)

    @property
    def classes(self):
        """A list of classes found by this factory"""
        return self._classes

    def compliant_classes(self, spec):
        """Return classes from our hierarchy, which match spec."""
        compliant = [ c for c in self.classes if c.supports(spec) ]
        return sorted(compliant, key=lambda c: c.supports(spec), reverse=True)

    def produce(self, spec, *args, **kw):
        """Creates an object of class matching spec. Raises FactoryError if
        there is no class compatible with specs."""
        classes = self.compliant_classes(spec)
        if not classes:
            raise FactoryError("could not find class to produce an object")
        klass = classes[0]
        return klass(klass.adjust(spec), *args, **kw)

    def produce_all(self, spec, *args, **kw):
        classes = self.compliant_classes(spec)
        return tuple(c(c.adjust(spec), *args, **kw) for c in classes)

    def _find_classes(self, **kw):
        p = lambda x : inspect.isclass(x) and \
                       issubclass(x, self._base) and \
                       x is not self._base and \
                       not inspect.isabstract(x)
        modules = kw.get('search', [self._base.__module__])
        if isinstance(modules, str) or inspect.ismodule(modules):
            modules = [modules]
        classes = []
        for mod in modules:
            if isinstance(mod,str):
                mod = sys.modules[mod]
            classes += [c for n, c in inspect.getmembers(mod, p)]
        return classes


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
