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
        """Check if an instance can be created from spec.

           Shall return positive number if

                cls(*cls.specargs(spec),..., **{**cls.speckwargs(spec), ...})

           is supposed to return valid object. Otherwise, should return a value
           which evaluates to False in boolean context.

           Classes, which declare to support given spec, get sorted by
           cls.supports(spec) in descending order and a class with highest
           score is selected by factory.produce(spec) to create an instance.
        """
        pass

    @classmethod
    def specargs(cls, spec):
        """Extracts positional arguments for constructor."""
        return (spec,)

    @classmethod
    def speckwargs(cls, spec):
        """Extracts keyword arguments for constructor."""
        return dict()


class Factory(object):
    """Given a base class and an abstract specification of an instance, it
    selects a subclass which best matches specification and creates an instance
    of this subclass. The job of specification matching is delegated to
    subclasses of FactorySubject."""

    @classmethod
    def instances(cls):
        """Dictionary which maps product base classes to factory objects"""
        if not hasattr(cls, '_instances'):
            cls._instances = dict()
        return cls._instances

    @classmethod
    def of(cls, base, **kw):
        """Returns a factory for a family of objects having a common base
        class"""
        if not inspect.isclass(base):
            raise TypeError("%s.of() argument 1 must be a class, %s provided" %
                            (cls.__name__, repr(base)))
        elif not issubclass(base, FactorySubject):
            raise TypeError(("%s.of() argument 1 must be a subclass of " +
                             "FactorySubject, %s provided") %
                            (cls.__name__, repr(base)))
        instances = cls.instances()
        if base not in instances:
            instances[base] = cls(base, **kw)
        return instances[base]

    def __init__(self, base, **kw):
        self._base = base
        self._classes = self._find_classes(**kw)

    @property
    def classes(self):
        """A list of classes found by this factory"""
        return self._classes

    def compliant_classes(self, spec):
        """Return classes from our hierarchy, which match spec."""
        tuples = [(klass, klass.supports(spec)) for klass in self.classes]
        tuples = filter(lambda x: bool(x[1]), tuples)
        tuples = sorted(tuples, key=lambda x: x[1], reverse=True)
        return [t[0] for t in tuples]

    def produce(self, spec, *args, **kw):
        """Creates an object of class matching spec. Raises FactoryError if
        there is no class compatible with specs."""
        classes = self.compliant_classes(spec)
        if not classes:
            raise FactoryError("could not find class to produce an object")
        klass = classes[0]
        return klass(*(tuple(klass.specargs(spec)) + tuple(args)),
                     **dict(klass.speckwargs(spec), **kw))

    def produce_all(self, spec, *args, **kw):
        classes = self.compliant_classes(spec)
        return tuple(klass(*(tuple(klass.specargs(spec)) + tuple(args)),
                           **dict(klass.speckwargs(spec), **kw))
                     for klass in classes)

    def _find_classes(self, **kw):
        def qualify(sym):
            return inspect.isclass(sym) and issubclass(sym, self._base) and \
                   not inspect.isabstract(sym)

        namespaces = kw.get('search', [self._base.__module__])
        if isinstance(namespaces, (str, dict)) or inspect.ismodule(namespaces):
            namespaces = [namespaces]
        classes = []
        for ns in namespaces:
            if isinstance(ns, dict):
                classes += [v for k, v in ns.items() if qualify(v)]
            else:
                if isinstance(ns, str):
                    ns = sys.modules[ns]
                classes += [c for n, c in inspect.getmembers(ns, qualify)]
        return classes


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
