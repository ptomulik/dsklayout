#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import unittest.mock as mock

import dsklayout.util.factory_ as factory_

class Test__FactoryError(unittest.TestCase):

    def test__issubclass__Exception(self):
        self.assertTrue(issubclass(factory_.FactoryError, Exception))

class Test__FactorySubject(unittest.TestCase):

    def test__is_abstract(self):
        with self.assertRaises(TypeError) as context:
            factory_.FactorySubject()
        self.assertIn('abstract', str(context.exception))

    def test__subclass_1(self):
        class T(factory_.FactorySubject):
            @classmethod
            def supports(cls, spec):
                return super().supports(spec)

        self.assertIsNone(T.supports('foo'))
        self.assertEqual(T.specargs('foo'), ('foo',))
        self.assertEqual(T.speckwargs('foo'), dict())

    def test__subclass(self):
        class T(factory_.FactorySubject):
            @classmethod
            def supports(cls, spec):
                return super().supports(spec)

        self.assertIsNone(T.supports('foo'))
        self.assertEqual(T.specargs('foo'), ('foo',))
        self.assertEqual(T.speckwargs('foo'), dict())

class Test__Factory(unittest.TestCase):

    def test__of__TypeError_1(self):
        with self.assertRaises(TypeError) as context:
            factory_.Factory.of('foo')
        self.assertEqual('Factory.of() argument 1 must be a class, %s provided'
                         % repr('foo'), str(context.exception))

    def test__of__TypeError_3(self):
        class T: pass
        with self.assertRaises(TypeError) as context:
            factory_.Factory.of(T)
        self.assertEqual(("Factory.of() argument 1 must be a subclass of " +
                          "FactorySubject, %s provided") % repr(T),
                         str(context.exception))

    def test__of__1(self):
        class T(factory_.FactorySubject):
            @classmethod
            def supports(self, spec):
                return True

        factory = factory_.Factory.of(T)
        self.assertIsInstance(factory, factory_.Factory)
        self.assertIs(factory_.Factory.of(T), factory)

    def test__classes__1(self):
        class T(factory_.FactorySubject):
            @classmethod
            def supports(self, spec):
                pass

        class T1(T):
            @classmethod
            def supports(self, spec):
                pass

        class T2(T):
            def __init__(self, spec):
                pass
            @classmethod
            def supports(self, spec):
                pass

        factory = factory_.Factory.of(T, search=locals())
        self.assertIn(T, factory.classes)
        self.assertIn(T1, factory.classes)
        self.assertIn(T2, factory.classes)

    def test__classes__2(self):
        class T(factory_.FactorySubject):
            pass

        class T1(T):
            @classmethod
            def supports(self, spec):
                pass

        class T2(T):
            def __init__(self, spec):
                pass
            @classmethod
            def supports(self, spec):
                pass

        factory = factory_.Factory.of(T, search=locals())
        self.assertNotIn(T, factory.classes)  # abstract
        self.assertIn(T1, factory.classes)
        self.assertIn(T2, factory.classes)

    def test__classes__3(self):
        class T(factory_.FactorySubject):
            pass

        class T1(T):
            @classmethod
            def supports(self, spec):
                pass

        class T2(object):
            @classmethod
            def supports(self, spec):
                pass

        factory = factory_.Factory.of(T, search=locals())
        self.assertNotIn(T, factory.classes)  # abstract
        self.assertIn(T1, factory.classes)
        self.assertNotIn(T2, factory.classes)  # not a subclass of FactorySubject

    def test__compliant_classess__1(self):
        class T(factory_.FactorySubject):
            @classmethod
            def supports(self, spec):
                return isinstance(spec, int) and spec > 10

        class T1(T):
            @classmethod
            def supports(self, spec):
                return isinstance(spec, int)

        class T2(T):
            @classmethod
            def supports(self, spec):
                return isinstance(spec, str)

        factory = factory_.Factory.of(T, search=locals())
        self.assertEqual(factory.compliant_classes(None), [])
        self.assertEqual(factory.compliant_classes('a'), [T2])
        self.assertEqual(factory.compliant_classes(8), [T1])
        self.assertEqual(list(sorted(factory.compliant_classes(11), key=lambda c: c.__name__)), [T, T1])

    def test__produce__1(self):
        class T(factory_.FactorySubject):
            def __init__(self, spec, *args, **kw):
                self.spec = spec
                self.args = args
                self.kw = kw
            @classmethod
            def supports(self, spec):
                return 2 if isinstance(spec, int) and spec > 9 else False

        class T1(T):
            @classmethod
            def supports(self, spec):
                return 1 if isinstance(spec, int) else False

        class T2(T):
            @classmethod
            def supports(self, spec):
                return 1 if isinstance(spec, str) else False

        class T3(T):
            @classmethod
            def supports(self, spec):
                return 2 if isinstance(spec, int) and spec > 6 else False

        factory = factory_.Factory.of(T, search=locals())
        foo = factory.produce('foo', 'A', 'B', c='C')
        two = factory.produce(2, 'A', 'B', c='C')
        ten = factory.produce(10, 'A', 'B', c='C')

        self.assertIs(foo.__class__, T2)
        self.assertIs(two.__class__, T1)
        self.assertIn(ten.__class__, [T, T3])

        self.assertEqual(foo.spec, 'foo')
        self.assertEqual(two.spec, 2)
        self.assertEqual(ten.spec, 10)

        self.assertEqual(foo.args, ('A', 'B'))
        self.assertEqual(two.args, ('A', 'B'))
        self.assertEqual(ten.args, ('A', 'B'))
        self.assertEqual(foo.kw, {'c': 'C'})
        self.assertEqual(two.kw, {'c': 'C'})
        self.assertEqual(ten.kw, {'c': 'C'})

    def test__produce_all__1(self):
        class T(factory_.FactorySubject):
            def __init__(self, spec, *args, **kw):
                self.spec = spec
                self.args = args
                self.kw = kw
            @classmethod
            def supports(self, spec):
                return 2 if isinstance(spec, int) and spec > 9 else False

        class T1(T):
            @classmethod
            def supports(self, spec):
                return 1 if isinstance(spec, int) else False

        class T2(T):
            @classmethod
            def supports(self, spec):
                return 1 if isinstance(spec, str) else False

        class T3(T):
            @classmethod
            def supports(self, spec):
                return 2 if isinstance(spec, int) and spec > 5 else False

        factory = factory_.Factory.of(T, search=locals())
        foo = factory.produce_all('foo', 'A', 'B', c='C')
        two = factory.produce_all(2, 'A', 'B', c='C')
        six = factory.produce_all(6, 'A', 'B', c='C')

        self.assertEqual(len(foo), 1)
        self.assertEqual(len(two), 1)
        self.assertEqual(len(six), 2)

        self.assertIs(foo[0].__class__, T2)
        self.assertIs(two[0].__class__, T1)
        self.assertIn(six[0].__class__, [T1, T3])
        if six[0].__class__ is T1:
            self.assertIs(six[1].__class__, T3)
        else:
            self.assertIs(six[1].__class__, T1)

        self.assertEqual(foo[0].spec, 'foo')
        self.assertEqual(two[0].spec, 2)
        self.assertEqual(six[0].spec, 6)
        self.assertEqual(six[1].spec, 6)

        self.assertEqual(foo[0].args, ('A', 'B'))
        self.assertEqual(two[0].args, ('A', 'B'))
        self.assertEqual(six[0].args, ('A', 'B'))
        self.assertEqual(six[1].args, ('A', 'B'))
        self.assertEqual(foo[0].kw, {'c': 'C'})
        self.assertEqual(two[0].kw, {'c': 'C'})
        self.assertEqual(six[0].kw, {'c': 'C'})
        self.assertEqual(six[1].kw, {'c': 'C'})

if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
