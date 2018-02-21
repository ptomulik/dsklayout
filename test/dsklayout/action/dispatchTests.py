#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import unittest.mock as mock

from dsklayout.action.dispatch_ import *

class Test__Dispatch(unittest.TestCase):

    @property
    def classes(self):
        if not hasattr(self,'_classes'):
            A1 = type("A1", (object,), dict())
            A2 = type("A2", (object,), dict())
            A3 = type("A3", (object,), dict())
            A4 = type("A4", (object,), dict())
            B1 = type("B1", (A1,A2), dict())
            B2 = type("B2", (A3,A4), dict())
            C  = type("C", (B1, B2), dict())
            self._classes = type("Classes", (object,), {
                'A1': A1, 'A2': A2, 'A3': A3, 'A4': A4,
                'B1': B1, 'B2': B2,
                'C': C
            })
        return self._classes

    def test__on__int_01(self):
        @dispatch.on(1)
        def func(a, b, c):
            return "func(%s,%s,%s)" % (repr(a), repr(b), repr(c))
        self.assertEqual(func.impl._arg_index, 1)
        self.assertEqual(func.impl._arg_name, 'b')
        self.assertTrue(callable(func.impl._default))
        self.assertEqual(func.impl._overloads, dict())
        self.assertEqual(func(1,2,3), "func(1,2,3)")

    def test__on__int_02(self):
        with self.assertRaises(ValueError) as context:
            @dispatch.on(-1)
            def func(a, b, c): pass
        self.assertEqual("negative argument index: -1", str(context.exception))

    def test__on__int_03(self):
        with self.assertRaises(ValueError) as context:
            @dispatch.on(3)
            def func(a, b, c): pass
        self.assertEqual("func() takes 3 positional arguments (indices 0 " +
                         "through 2), but argument index 3 was selected " +
                         "for dispatching", str(context.exception))

    def test__on__int_04(self):
        with self.assertRaises(ValueError) as context:
            @dispatch.on(3)
            def func(a, b, c, *args): pass
        self.assertEqual("func() takes 3 positional arguments (indices 0 " +
                         "through 2) and variadic arguments (unused by " +
                         "dispatch), however, argument index 3 was selected " +
                         "for dispatching", str(context.exception))

    def test__on__int_05(self):
        @dispatch.on(3, varargs=True)
        def func(a, b, c, *args):
            return "func(%s,%s,%s,*%s)" % (repr(a), repr(b), repr(c), repr(args))
        self.assertEqual(func.impl._arg_index, 3)
        self.assertIsNone(func.impl._arg_name)
        self.assertTrue(callable(func.impl._default))
        self.assertEqual(func.impl._overloads, dict())
        self.assertEqual(func(1,2,3,4), "func(1,2,3,*%s)" % repr((4,)))
        self.assertEqual(func(1,2,3), "func(1,2,3,*%s)" % repr(()))

    def test__on__int_06(self):
        @dispatch.on(2)
        def func(a, b, c):
            return "func(%s,%s,%s)" % (repr(a), repr(b), repr(c))
        self.assertEqual(func.impl._arg_index, 2)
        self.assertEqual(func.impl._arg_name, 'c')
        self.assertTrue(callable(func.impl._default))
        self.assertEqual(func.impl._overloads, dict())
        self.assertEqual(func(1,2,3), "func(1,2,3)")
        with self.assertRaises(TypeError) as context:
            func(1,2)
        self.assertEqual("func() missing 1 required positional argument", str(context.exception))
        with self.assertRaises(TypeError) as context:
            func(1)
        self.assertEqual("func() missing 2 required positional arguments", str(context.exception))

    def test__on__str_01(self):
        @dispatch.on('b')
        def func(a, b, c):
            return "func(%s,%s,%s)" % (repr(a), repr(b), repr(c))
        self.assertEqual(func.impl._arg_index, 1)
        self.assertEqual(func.impl._arg_name, 'b')
        self.assertTrue(callable(func.impl._default))
        self.assertEqual(func.impl._overloads, dict())
        self.assertEqual(func(1,2,3), "func(1,2,3)")

    def test__on__str_02(self):
        with self.assertRaises(ValueError) as context:
            @dispatch.on('d')
            def func(a, b, c): pass
        self.assertEqual(("func() has no positional argument named %s " +
                          "and takes no keyword arguments") % repr('d'),
                         str(context.exception))

    def test__on__str_03(self):
        with self.assertRaises(ValueError) as context:
            @dispatch.on('d', kwargs=True)
            def func(a, b, c): pass
        self.assertEqual(("func() has no positional argument named %s " +
                          "and takes no keyword arguments") % repr('d'),
                         str(context.exception))

    def test__on__str_04(self):
        with self.assertRaises(ValueError) as context:
            @dispatch.on('d')
            def func(a, b, c): pass
        self.assertEqual(("func() has no positional argument named %s " +
                          "and takes no keyword arguments") % repr('d'),
                         str(context.exception))

    def test__on__str_05(self):
        with self.assertRaises(ValueError) as context:
            @dispatch.on('d')
            def func(a, b, c, **kw): pass
        self.assertEqual(("func() has no positional argument named %s " +
                          "and keyword arguments are disabled") % repr('d'),
                         str(context.exception))

    def test__on__str_06(self):
        @dispatch.on('d', kwargs=True)
        def func(a, b, c, **kw):
            return "func(%s,%s,%s,**%s)" % (repr(a), repr(b), repr(c), repr(kw))
        self.assertIsNone(func.impl._arg_index)
        self.assertEqual(func.impl._arg_name, 'd')
        self.assertTrue(callable(func.impl._default))
        self.assertEqual(func.impl._overloads, dict())
        self.assertEqual(func(1,2,3, d = 2), "func(1,2,3,**%s)" % repr({'d':2}))
        self.assertEqual(func(1,2,3), "func(1,2,3,**%s)" % repr(dict()))

    def test__on__None(self):
        with self.assertRaises(TypeError) as context:
            @dispatch.on(None)
            def func(): pass
        self.assertEqual("dispatch.on() argument 1 must be either int or str, not %s"
                         % repr(None), str(context.exception))

    def test__when__nontype(self):
        _ = self.classes

        @dispatch.on(0)
        def func(x): pass

        with self.assertRaises(TypeError) as context:
            @func.when('func')
            def func(x): pass
        self.assertEqual("dispatch.when() argument 1 must be a type, not %s"
                         % repr('func'), str(context.exception))

    def test__when__nonclass(self):
        _ = self.classes

        @dispatch.on(0)
        def func(x):
            return "func(%s)" % repr(x)

        @func.when(int)
        def func(x):
            return "func<int>(%s)" % repr(x)

        self.assertEqual(func('a'),  "func(%s)"      % repr('a'))
        self.assertEqual(func(2),    "func<int>(%s)" % repr(2))
        self.assertEqual(func(True), "func<int>(%s)" % repr(True))

    def test__when__missing_01(self):
        _ = self.classes

        @dispatch.on(0)
        def func(x): pass

        with self.assertRaises(TypeError) as context:
            @func.when(_.A1)
            def func(): pass
        self.assertEqual("argument index 0 was selected for dispatching, " +
                         "but func() takes no positional arguments",
                         str(context.exception))

    def test__when__missing_02(self):
        _ = self.classes

        @dispatch.on(1)
        def func(x,y): pass

        with self.assertRaises(TypeError) as context:
            @func.when(_.A1)
            def func(x): pass
        self.assertEqual("argument index 1 was selected for dispatching, " +
                         "but func() takes only 1 positional argument (index 0)",
                         str(context.exception))

    def test__when__missing_03(self):
        _ = self.classes

        @dispatch.on(2)
        def func(x,y,z): pass

        with self.assertRaises(TypeError) as context:
            @func.when(_.A1)
            def func(x,y): pass
        self.assertEqual("argument index 2 was selected for dispatching, " +
                         "but func() takes only 2 positional arguments " +
                         "(indices 0 through 1)", str(context.exception))

    def test__when__RuntimeError_01(self):
        _ = self.classes

        @dispatch.on(0)
        def func(x): pass

        func.impl._arg_index = -1

        with self.assertRaises(RuntimeError) as context:
            @func.when(_.A1)
            def func(x): pass
        self.assertEqual("bug: negative arg_index: -1", str(context.exception))

    def test__when__RuntimeError_02(self):
        _ = self.classes

        @dispatch.on(0)
        def func(x): pass

        func.impl._arg_index = None
        func.impl._arg_name = None

        with self.assertRaises(RuntimeError) as context:
            @func.when(_.A1)
            def func(x): pass
        self.assertEqual("bug: both arg_index and arg_name are None", str(context.exception))

    def test__when__on__str_01(self):
        _ = self.classes

        @dispatch.on('x')
        def func(x):
            return "func(%s)" % repr(x)

        @func.when(_.A1)
        def func(x):
            return "func<A1>(%s)" % repr(x)

        a1 = _.A1()
        self.assertEqual(func(1), "func(%s)" % repr(1))
        self.assertEqual(func(a1), "func<A1>(%s)" % repr(a1))

    def test__when__on__str_02(self):
        _ = self.classes

        @dispatch.on('y', kwargs=True)
        def func(x,**kw):
            return "func(%s,**%s)" % (repr(x),repr(kw))

        with self.assertRaises(TypeError) as context:
            @func.when(_.A1)
            def func(x):
                return "func<A1>(%s)" % repr(x)
        self.assertEqual("argument named 'y' was selected for dispatching, " +
                         "but func() has no positional argument named " +
                         "'y' and takes no keyword arguments", str(context.exception))

    def test__when__on__str_03(self):
        _ = self.classes

        @dispatch.on('y', kwargs=True)
        def func(x,**kw):
            return "func(%s,**%s)" % (repr(x),repr(kw))

        @func.when(_.A1)
        def func(x,**kw):
            return "func<A1>(%s,**%s)" % (repr(x),repr(kw))

        a1 = _.A1()
        b1 = _.B1()
        self.assertEqual(func(1,y=a1), "func<A1>(%s,**%s)" % (repr(1), repr({'y': a1})))
        self.assertEqual(func(1,y=b1), "func<A1>(%s,**%s)" % (repr(1), repr({'y': b1})))

    def test__when__on__str_04(self):
        _ = self.classes

        @dispatch.on('y', kwargs=True)
        def func(x,**kw):
            return "func(%s,**%s)" % (repr(x),repr(kw))

        @func.when(_.A1)
        def func(x,y):
            return "func<A1>(%s,%s)" % (repr(x),repr(y))

        a1 = _.A1()
        b1 = _.B1()
        self.assertEqual(func(1,y=a1), "func<A1>(%s,%s)" % (repr(1), repr(a1)))
        self.assertEqual(func(1,y=b1), "func<A1>(%s,%s)" % (repr(1), repr(b1)))

    def test__dispatch__01(self):
        _ = self.classes

        @dispatch.on(0)
        def func(x):
            return "func(%s)" % repr(x)

        @func.when(_.A1)
        def func(x):
            return "func<A1>(%s)" % repr(x)

        a1, a2, a3, a4, b1, b2, c = (_.A1(), _.A2(), _.A3(), _.A4(), _.B1(), _.B2(), _.C())

        self.assertEqual(func(1), "func(1)")
        self.assertEqual(func(a1), "func<A1>(%s)" % repr(a1))
        self.assertEqual(func(a2), "func(%s)"     % repr(a2))
        self.assertEqual(func(a3), "func(%s)"     % repr(a3))
        self.assertEqual(func(a4), "func(%s)"     % repr(a4))
        self.assertEqual(func(b1), "func<A1>(%s)" % repr(b1))
        self.assertEqual(func(b2), "func(%s)"     % repr(b2))
        self.assertEqual(func(c),  "func<A1>(%s)" % repr(c))

    def test__dispatch__02(self):
        _ = self.classes

        @dispatch.on(0)
        def func(x):
            return "func(%s)" % repr(x)

        @func.when(_.A2)
        def func(x):
            return "func<A2>(%s)" % repr(x)

        a1, a2, a3, a4, b1, b2, c = (_.A1(), _.A2(), _.A3(), _.A4(), _.B1(), _.B2(), _.C())

        self.assertEqual(func(1), "func(1)")
        self.assertEqual(func(a1), "func(%s)"     % repr(a1))
        self.assertEqual(func(a2), "func<A2>(%s)" % repr(a2))
        self.assertEqual(func(a3), "func(%s)"     % repr(a3))
        self.assertEqual(func(a4), "func(%s)"     % repr(a4))
        self.assertEqual(func(b1), "func<A2>(%s)" % repr(b1))
        self.assertEqual(func(b2), "func(%s)"     % repr(b2))
        self.assertEqual(func(c),  "func<A2>(%s)" % repr(c))

    def test__dispatch__03(self):
        _ = self.classes

        @dispatch.on(0)
        def func(x):
            return "func(%s)" % repr(x)

        @func.when(_.A3)
        def func(x):
            return "func<A3>(%s)" % repr(x)

        a1, a2, a3, a4, b1, b2, c = (_.A1(), _.A2(), _.A3(), _.A4(), _.B1(), _.B2(), _.C())

        self.assertEqual(func(1), "func(1)")
        self.assertEqual(func(a1), "func(%s)"     % repr(a1))
        self.assertEqual(func(a2), "func(%s)"     % repr(a2))
        self.assertEqual(func(a3), "func<A3>(%s)" % repr(a3))
        self.assertEqual(func(a4), "func(%s)"     % repr(a4))
        self.assertEqual(func(b1), "func(%s)"     % repr(b1))
        self.assertEqual(func(b2), "func<A3>(%s)" % repr(b2))
        self.assertEqual(func(c),  "func<A3>(%s)" % repr(c))

    def test__dispatch__04(self):
        _ = self.classes

        @dispatch.on(0)
        def func(x):
            return "func(%s)" % repr(x)

        @func.when(_.A4)
        def func(x):
            return "func<A4>(%s)" % repr(x)

        a1, a2, a3, a4, b1, b2, c = (_.A1(), _.A2(), _.A3(), _.A4(), _.B1(), _.B2(), _.C())

        self.assertEqual(func(1), "func(1)")
        self.assertEqual(func(a1), "func(%s)"     % repr(a1))
        self.assertEqual(func(a2), "func(%s)"     % repr(a2))
        self.assertEqual(func(a3), "func(%s)"     % repr(a3))
        self.assertEqual(func(a4), "func<A4>(%s)" % repr(a4))
        self.assertEqual(func(b1), "func(%s)"     % repr(b1))
        self.assertEqual(func(b2), "func<A4>(%s)" % repr(b2))
        self.assertEqual(func(c),  "func<A4>(%s)" % repr(c))

    def test__dispatch__05(self):
        _ = self.classes

        @dispatch.on(0)
        def func(x):
            return "func(%s)" % repr(x)

        @func.when(_.B1)
        def func(x):
            return "func<B1>(%s)" % repr(x)

        a1, a2, a3, a4, b1, b2, c = (_.A1(), _.A2(), _.A3(), _.A4(), _.B1(), _.B2(), _.C())

        self.assertEqual(func(1), "func(1)")
        self.assertEqual(func(a1), "func(%s)"     % repr(a1))
        self.assertEqual(func(a2), "func(%s)"     % repr(a2))
        self.assertEqual(func(a3), "func(%s)"     % repr(a3))
        self.assertEqual(func(a4), "func(%s)"     % repr(a4))
        self.assertEqual(func(b1), "func<B1>(%s)" % repr(b1))
        self.assertEqual(func(b2), "func(%s)"     % repr(b2))
        self.assertEqual(func(c),  "func<B1>(%s)" % repr(c))

    def test__dispatch__06(self):
        _ = self.classes

        @dispatch.on(0)
        def func(x):
            return "func(%s)" % repr(x)

        @func.when(_.B2)
        def func(x):
            return "func<B2>(%s)" % repr(x)

        a1, a2, a3, a4, b1, b2, c = (_.A1(), _.A2(), _.A3(), _.A4(), _.B1(), _.B2(), _.C())

        self.assertEqual(func(1), "func(1)")
        self.assertEqual(func(a1), "func(%s)"     % repr(a1))
        self.assertEqual(func(a2), "func(%s)"     % repr(a2))
        self.assertEqual(func(a3), "func(%s)"     % repr(a3))
        self.assertEqual(func(a4), "func(%s)"     % repr(a4))
        self.assertEqual(func(b1), "func(%s)"     % repr(b1))
        self.assertEqual(func(b2), "func<B2>(%s)" % repr(b2))
        self.assertEqual(func(c),  "func<B2>(%s)" % repr(c))

    def test__dispatch__07(self):
        _ = self.classes

        @dispatch.on(0)
        def func(x):
            return "func(%s)" % repr(x)

        @func.when(_.C)
        def func(x):
            return "func<C>(%s)" % repr(x)

        a1, a2, a3, a4, b1, b2, c = (_.A1(), _.A2(), _.A3(), _.A4(), _.B1(), _.B2(), _.C())

        self.assertEqual(func(1), "func(1)")
        self.assertEqual(func(a1), "func(%s)"     % repr(a1))
        self.assertEqual(func(a2), "func(%s)"     % repr(a2))
        self.assertEqual(func(a3), "func(%s)"     % repr(a3))
        self.assertEqual(func(a4), "func(%s)"     % repr(a4))
        self.assertEqual(func(b1), "func(%s)"     % repr(b1))
        self.assertEqual(func(b2), "func(%s)"     % repr(b2))
        self.assertEqual(func(c),  "func<C>(%s)"  % repr(c))

    def test__dispatch__08(self):
        _ = self.classes

        @dispatch.on(0)
        def func(x):
            return "func(%s)" % repr(x)

        @func.when(_.A1)
        def func(x):
            return "func<A1>(%s)" % repr(x)

        @func.when(_.A2)
        def func(x):
            return "func<A2>(%s)" % repr(x)

        a1, a2, a3, a4, b1, b2, c = (_.A1(), _.A2(), _.A3(), _.A4(), _.B1(), _.B2(), _.C())

        self.assertEqual(func(1), "func(1)")
        self.assertEqual(func(a1), "func<A1>(%s)" % repr(a1))
        self.assertEqual(func(a2), "func<A2>(%s)" % repr(a2))
        self.assertEqual(func(a3), "func(%s)"     % repr(a3))
        self.assertEqual(func(a4), "func(%s)"     % repr(a4))
        self.assertEqual(func(b1), "func<A1>(%s)" % repr(b1))
        self.assertEqual(func(b2), "func(%s)"     % repr(b2))
        self.assertEqual(func(c),  "func<A1>(%s)" % repr(c))

    def test__dispatch__09(self):
        _ = self.classes

        @dispatch.on(0)
        def func(x):
            return "func(%s)" % repr(x)

        @func.when(_.A3)
        def func(x):
            return "func<A3>(%s)" % repr(x)

        @func.when(_.A4)
        def func(x):
            return "func<A4>(%s)" % repr(x)

        a1, a2, a3, a4, b1, b2, c = (_.A1(), _.A2(), _.A3(), _.A4(), _.B1(), _.B2(), _.C())

        self.assertEqual(func(1), "func(1)")
        self.assertEqual(func(a1), "func(%s)"     % repr(a1))
        self.assertEqual(func(a2), "func(%s)"     % repr(a2))
        self.assertEqual(func(a3), "func<A3>(%s)" % repr(a3))
        self.assertEqual(func(a4), "func<A4>(%s)" % repr(a4))
        self.assertEqual(func(b1), "func(%s)"     % repr(b1))
        self.assertEqual(func(b2), "func<A3>(%s)" % repr(b2))
        self.assertEqual(func(c),  "func<A3>(%s)" % repr(c))

    def test__dispatch__10(self):
        _ = self.classes

        @dispatch.on(0)
        def func(x):
            return "func(%s)" % repr(x)

        @func.when(_.A1)
        def func(x):
            return "func<A1>(%s)" % repr(x)

        @func.when(_.A2)
        def func(x):
            return "func<A2>(%s)" % repr(x)

        @func.when(_.A3)
        def func(x):
            return "func<A3>(%s)" % repr(x)

        @func.when(_.A4)
        def func(x):
            return "func<A4>(%s)" % repr(x)

        a1, a2, a3, a4, b1, b2, c = (_.A1(), _.A2(), _.A3(), _.A4(), _.B1(), _.B2(), _.C())

        self.assertEqual(func(1), "func(1)")
        self.assertEqual(func(a1), "func<A1>(%s)" % repr(a1))
        self.assertEqual(func(a2), "func<A2>(%s)" % repr(a2))
        self.assertEqual(func(a3), "func<A3>(%s)" % repr(a3))
        self.assertEqual(func(a4), "func<A4>(%s)" % repr(a4))
        self.assertEqual(func(b1), "func<A1>(%s)" % repr(b1))
        self.assertEqual(func(b2), "func<A3>(%s)" % repr(b2))
        self.assertEqual(func(c),  "func<A1>(%s)" % repr(c))

    def test__dispatch__11(self):
        _ = self.classes

        @dispatch.on(0)
        def func(x):
            return "func(%s)" % repr(x)

        @func.when(_.A2)
        def func(x):
            return "func<A2>(%s)" % repr(x)

        @func.when(_.A4)
        def func(x):
            return "func<A4>(%s)" % repr(x)

        a1, a2, a3, a4, b1, b2, c = (_.A1(), _.A2(), _.A3(), _.A4(), _.B1(), _.B2(), _.C())

        self.assertEqual(func(1), "func(1)")
        self.assertEqual(func(a1), "func(%s)"     % repr(a1))
        self.assertEqual(func(a2), "func<A2>(%s)" % repr(a2))
        self.assertEqual(func(a3), "func(%s)"     % repr(a3))
        self.assertEqual(func(a4), "func<A4>(%s)" % repr(a4))
        self.assertEqual(func(b1), "func<A2>(%s)" % repr(b1))
        self.assertEqual(func(b2), "func<A4>(%s)" % repr(b2))
        self.assertEqual(func(c),  "func<A2>(%s)" % repr(c))

    def test__dispatch__12(self):
        _ = self.classes

        @dispatch.on(0)
        def func(x):
            return "func(%s)" % repr(x)

        @func.when(_.B1)
        def func(x):
            return "func<B1>(%s)" % repr(x)

        @func.when(_.B2)
        def func(x):
            return "func<B2>(%s)" % repr(x)

        a1, a2, a3, a4, b1, b2, c = (_.A1(), _.A2(), _.A3(), _.A4(), _.B1(), _.B2(), _.C())

        self.assertEqual(func(1), "func(1)")
        self.assertEqual(func(a1), "func(%s)"     % repr(a1))
        self.assertEqual(func(a2), "func(%s)"     % repr(a2))
        self.assertEqual(func(a3), "func(%s)"     % repr(a3))
        self.assertEqual(func(a4), "func(%s)"     % repr(a4))
        self.assertEqual(func(b1), "func<B1>(%s)" % repr(b1))
        self.assertEqual(func(b2), "func<B2>(%s)" % repr(b2))
        self.assertEqual(func(c),  "func<B1>(%s)" % repr(c))

    def test__dispatch__13(self):
        _ = self.classes

        @dispatch.on(0)
        def func(x):
            return "func(%s)" % repr(x)
        @func.when(_.A1)
        def func(x):
            return "func<A1>(%s)" % repr(x)
        @func.when(_.A2)
        def func(x):
            return "func<A2>(%s)" % repr(x)
        @func.when(_.A3)
        def func(x):
            return "func<A3>(%s)" % repr(x)
        @func.when(_.A4)
        def func(x):
            return "func<A4>(%s)" % repr(x)
        @func.when(_.B1)
        def func(x):
            return "func<B1>(%s)" % repr(x)
        @func.when(_.B2)
        def func(x):
            return "func<B2>(%s)" % repr(x)
        @func.when(_.C)
        def func(x):
            return "func<C>(%s)" % repr(x)

        a1, a2, a3, a4, b1, b2, c = (_.A1(), _.A2(), _.A3(), _.A4(), _.B1(), _.B2(), _.C())

        self.assertEqual(func(1),  "func(1)")
        self.assertEqual(func(a1), "func<A1>(%s)" % repr(a1))
        self.assertEqual(func(a2), "func<A2>(%s)" % repr(a2))
        self.assertEqual(func(a3), "func<A3>(%s)" % repr(a3))
        self.assertEqual(func(a4), "func<A4>(%s)" % repr(a4))
        self.assertEqual(func(b1), "func<B1>(%s)" % repr(b1))
        self.assertEqual(func(b2), "func<B2>(%s)" % repr(b2))
        self.assertEqual(func(c),  "func<C>(%s)"  % repr(c))

    def test__dispatch__method__01(self):
        _ = self.classes

        class T(object):
            @dispatch.on(1)
            def func(self, x):
                return "%s.func(%s)" % (repr(self), repr(x))
            @func.when(_.A1)
            def func(self, x):
                return "%s.func<A1>(%s)" % (repr(self), repr(x))
            @func.when(_.A2)
            def func(self, x):
                return "%s.func<A2>(%s)" % (repr(self), repr(x))
            @func.when(_.A3)
            def func(self, x):
                return "%s.func<A3>(%s)" % (repr(self), repr(x))
            @func.when(_.A4)
            def func(self, x):
                return "%s.func<A4>(%s)" % (repr(self), repr(x))
            @func.when(_.B1)
            def func(self, x):
                return "%s.func<B1>(%s)" % (repr(self), repr(x))
            @func.when(_.B2)
            def func(self, x):
                return "%s.func<B2>(%s)" % (repr(self), repr(x))
            @func.when(_.C)
            def func(self, x):
                return "%s.func<C>(%s)" % (repr(self), repr(x))

        a1, a2, a3, a4, b1, b2, c = (_.A1(), _.A2(), _.A3(), _.A4(), _.B1(), _.B2(), _.C())
        t = T()

        self.assertEqual(t.func(1),  "%s.func(1)" % repr(t))
        self.assertEqual(t.func(a1), "%s.func<A1>(%s)" % (repr(t), repr(a1)))
        self.assertEqual(t.func(a2), "%s.func<A2>(%s)" % (repr(t), repr(a2)))
        self.assertEqual(t.func(a3), "%s.func<A3>(%s)" % (repr(t), repr(a3)))
        self.assertEqual(t.func(a4), "%s.func<A4>(%s)" % (repr(t), repr(a4)))
        self.assertEqual(t.func(b1), "%s.func<B1>(%s)" % (repr(t), repr(b1)))
        self.assertEqual(t.func(b2), "%s.func<B2>(%s)" % (repr(t), repr(b2)))
        self.assertEqual(t.func(c),  "%s.func<C>(%s)"  % (repr(t), repr(c)))

    def test__dispatch__classmethod__01(self):
        _ = self.classes

        class T(object):
            @classmethod
            @dispatch.on(1)
            def func(cls, x):
                return "%s.func(%s)" % (repr(cls), repr(x))
            @classmethod
            @dispatch.when(_.A1)
            def func(cls, x):
                return "%s.func<A1>(%s)" % (repr(cls), repr(x))
            @classmethod
            @dispatch.when(_.A2)
            def func(cls, x):
                return "%s.func<A2>(%s)" % (repr(cls), repr(x))
            @classmethod
            @dispatch.when(_.A3)
            def func(cls, x):
                return "%s.func<A3>(%s)" % (repr(cls), repr(x))
            @classmethod
            @dispatch.when(_.A4)
            def func(cls, x):
                return "%s.func<A4>(%s)" % (repr(cls), repr(x))
            @classmethod
            @dispatch.when(_.B1)
            def func(cls, x):
                return "%s.func<B1>(%s)" % (repr(cls), repr(x))
            @classmethod
            @dispatch.when(_.B2)
            def func(cls, x):
                return "%s.func<B2>(%s)" % (repr(cls), repr(x))
            @classmethod
            @dispatch.when(_.C)
            def func(cls, x):
                return "%s.func<C>(%s)" % (repr(cls), repr(x))

        a1, a2, a3, a4, b1, b2, c = (_.A1(), _.A2(), _.A3(), _.A4(), _.B1(), _.B2(), _.C())
        t = T()

        self.assertEqual(t.func(1),  "%s.func(1)" % repr(T))
        self.assertEqual(t.func(a1), "%s.func<A1>(%s)" % (repr(T), repr(a1)))
        self.assertEqual(t.func(a2), "%s.func<A2>(%s)" % (repr(T), repr(a2)))
        self.assertEqual(t.func(a3), "%s.func<A3>(%s)" % (repr(T), repr(a3)))
        self.assertEqual(t.func(a4), "%s.func<A4>(%s)" % (repr(T), repr(a4)))
        self.assertEqual(t.func(b1), "%s.func<B1>(%s)" % (repr(T), repr(b1)))
        self.assertEqual(t.func(b2), "%s.func<B2>(%s)" % (repr(T), repr(b2)))
        self.assertEqual(t.func(c),  "%s.func<C>(%s)"  % (repr(T), repr(c)))

        self.assertEqual(T.func(1),  "%s.func(1)" % repr(T))
        self.assertEqual(T.func(a1), "%s.func<A1>(%s)" % (repr(T), repr(a1)))
        self.assertEqual(T.func(a2), "%s.func<A2>(%s)" % (repr(T), repr(a2)))
        self.assertEqual(T.func(a3), "%s.func<A3>(%s)" % (repr(T), repr(a3)))
        self.assertEqual(T.func(a4), "%s.func<A4>(%s)" % (repr(T), repr(a4)))
        self.assertEqual(T.func(b1), "%s.func<B1>(%s)" % (repr(T), repr(b1)))
        self.assertEqual(T.func(b2), "%s.func<B2>(%s)" % (repr(T), repr(b2)))
        self.assertEqual(T.func(c),  "%s.func<C>(%s)"  % (repr(T), repr(c)))

    def test__dispatch__staticmethod__01(self):
        _ = self.classes

        class T(object):
            @staticmethod
            @dispatch.on(0)
            def func(x):
                return "func(%s)" % repr(x)
            @staticmethod
            @dispatch.when(_.A1)
            def func(x):
                return "func<A1>(%s)" % repr(x)
            @staticmethod
            @dispatch.when(_.A2)
            def func(x):
                return "func<A2>(%s)" % repr(x)
            @staticmethod
            @dispatch.when(_.A3)
            def func(x):
                return "func<A3>(%s)" % repr(x)
            @staticmethod
            @dispatch.when(_.A4)
            def func(x):
                return "func<A4>(%s)" % repr(x)
            @staticmethod
            @dispatch.when(_.B1)
            def func(x):
                return "func<B1>(%s)" % repr(x)
            @staticmethod
            @dispatch.when(_.B2)
            def func(x):
                return "func<B2>(%s)" % repr(x)
            @staticmethod
            @dispatch.when(_.C)
            def func(x):
                return "func<C>(%s)" % repr(x)

        a1, a2, a3, a4, b1, b2, c = (_.A1(), _.A2(), _.A3(), _.A4(), _.B1(), _.B2(), _.C())
        t = T()

        self.assertEqual(T.func(1),  "func(1)")
        self.assertEqual(T.func(a1), "func<A1>(%s)" % repr(a1))
        self.assertEqual(T.func(a2), "func<A2>(%s)" % repr(a2))
        self.assertEqual(T.func(a3), "func<A3>(%s)" % repr(a3))
        self.assertEqual(T.func(a4), "func<A4>(%s)" % repr(a4))
        self.assertEqual(T.func(b1), "func<B1>(%s)" % repr(b1))
        self.assertEqual(T.func(b2), "func<B2>(%s)" % repr(b2))
        self.assertEqual(T.func(c),  "func<C>(%s)"  % repr(c))

if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
