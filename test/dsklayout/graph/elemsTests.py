#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest

import dsklayout.graph.elems_ as elems_

class Test__MISSING(unittest.TestCase):

    def test__MISSING(self):
        self.assertFalse(bool(elems_.MISSING))
        self.assertEqual(str(elems_.MISSING), 'MISSING')

class Test__Elems(unittest.TestCase):

    def test__init__0(self):
        elems = elems_.Elems()
        self.assertEqual(elems.data, dict())

    def test__init__1(self):
        elems = elems_.Elems(['x1', 'x2'])
        self.assertEqual(elems.data, {'x1': None, 'x2': None})

    def test__init__2(self):
        elems = elems_.Elems(['x1', 'x2', 'x1'])
        self.assertEqual(elems.data, {'x1': None, 'x2': None})

    def test__init__3(self):
        elems = elems_.Elems([('x1', 'X1'), ('x2', 'X2')])
        self.assertEqual(elems.data, {('x1','X1'): None, ('x2','X2'): None})

    def test__init__3_data_true(self):
        elems = elems_.Elems([('x1', 'X1'), ('x2', 'X2')], data=True)
        self.assertEqual(elems.data, {'x1': 'X1', 'x2': 'X2'})

    def test__init__4(self):
        elems = elems_.Elems({'x1': 'X1', 'x2': 'X2'})
        self.assertEqual(elems.data, {'x1': 'X1', 'x2': 'X2'})

    def test__init__4_data_false(self):
        elems = elems_.Elems({'x1': 'X1', 'x2': 'X2'}, data=False)
        self.assertEqual(elems.data, {('x1','X1'): None, ('x2','X2'): None})

    def test__contains__(self):
        elems = elems_.Elems({'x1': 'X1', 'x2': 'X2'})
        self.assertTrue('x1' in elems)
        self.assertTrue('x2' in elems)
        self.assertFalse('n3' in elems)
        self.assertFalse('X1' in elems)
        self.assertFalse('X2' in elems)

    def test__iter__(self):
        elems = elems_.Elems({'x1': 'X1', 'x2': 'X2'})
        self.assertEqual(list(iter(elems)), list(elems.data.keys()))

    def test__len__(self):
        elems = elems_.Elems({'x1': 'X1', 'x2': 'X2'})
        self.assertEqual(len(elems), 2)

    def test__repr__1(self):
        elems = elems_.Elems({'x1': 'X1', 'x2': 'X2'})
        self.assertEqual(repr(elems), "Elems(%s)" % repr(elems.data))

    def test__repr__2(self):
        elems = elems_.Elems()
        self.assertEqual(repr(elems), "Elems()")

    def test__getitem__1(self):
        elems = elems_.Elems({'x1': 'X1', 'x2': 'X2'})
        self.assertEqual(elems['x1'],'X1')
        self.assertEqual(elems['x2'],'X2')

    def test__getitem__2(self):
        elems = elems_.Elems()
        with self.assertRaises(KeyError):
            elems['x']

    def test__setitem__2(self):
        elems = elems_.Elems({'x1':  'X1'})
        elems['x1'] = '_X1_'
        elems['x2'] = '_X2_'
        self.assertEqual(elems.data, {'x1':  '_X1_', 'x2':  '_X2_'})

    def test__delitem__1(self):
        elems = elems_.Elems({'x1': 'X1', 'x2': 'X2'})
        del elems['x1']
        self.assertEqual(elems.data, {'x2':  'X2'})

    def test__delitem__2(self):
        elems = elems_.Elems({'x1': 'X1', 'x2': 'X2'})
        with self.assertRaises(KeyError):
            del elems['n3']

    def test__add__1(self):
        elems = elems_.Elems({'x1':  'X1'})
        elems.add('x1', '_X1_')
        elems.add('x2', '_X2_')
        self.assertEqual(elems.data, {'x1':  '_X1_', 'x2':  '_X2_'})

    def test__add__2(self):
        elems = elems_.Elems({'x1':  'X1'})
        elems.add('x1')
        elems.add('x2')
        self.assertEqual(elems.data, {'x1':  'X1', 'x2':  None})

    def test__discard__1(self):
        elems = elems_.Elems({'x1': 'X1', 'x2': 'X2'})
        elems.discard('x1')
        self.assertEqual(elems.data, {'x2':  'X2'})

    def test__discard__2(self):
        elems = elems_.Elems({'x1': 'X1', 'x2': 'X2'})
        elems.discard('n3')
        self.assertEqual(elems.data, {'x1':  'X1', 'x2':  'X2'})

    def test__clear(self):
        elems = elems_.Elems({'x1': 'X1', 'x2': 'X2'})
        elems.clear()
        self.assertEqual(elems.data, dict())

    def test__items(self):
        elems = elems_.Elems({'x1': 'X1', 'x2': 'X2'})
        self.assertEqual(list(elems.items()), list(elems.data.items()))

    def test__update__0(self):
        elems = elems_.Elems()
        self.assertEqual(elems.data, dict())

    def test__update__1(self):
        elems = elems_.Elems()
        elems.update(['x1', 'x2'])
        self.assertEqual(elems.data, {'x1': None, 'x2': None})

    def test__update__2(self):
        elems = elems_.Elems()
        elems.update(['x1', 'x2', 'x1'])
        self.assertEqual(elems.data, {'x1': None, 'x2': None})

    def test__update__3(self):
        elems = elems_.Elems()
        elems.update([('x1', 'X1'), ('x2', 'X2')])
        self.assertEqual(elems.data, {('x1','X1'): None, ('x2','X2'): None})

    def test__update__3_data_true(self):
        elems = elems_.Elems(['x1','x2'])
        elems.update([('x1', 'X1'), ('x2', 'X2')], data=True)
        self.assertEqual(elems.data, {'x1': 'X1', 'x2': 'X2'})

    def test__update__4(self):
        elems = elems_.Elems()
        elems.update({'x1': 'X1', 'x2': 'X2'})
        self.assertEqual(elems.data, {'x1': 'X1', 'x2': 'X2'})

    def test__update__4_data_false(self):
        elems = elems_.Elems()
        elems.update({'x1': 'X1', 'x2': 'X2'}, data=False)
        self.assertEqual(elems.data, {('x1','X1'): None, ('x2','X2'): None})

    def test__update__5(self):
        elems = elems_.Elems({'x1':  'X1', 'x2':'X2'})
        elems.update(['x1', 'x2', 'x3'])
        self.assertEqual(elems.data, {'x1': 'X1', 'x2': 'X2', 'x3':  None})

if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
