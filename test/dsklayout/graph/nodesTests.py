#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest

import dsklayout.graph.nodes_ as nodes_

class Test__Nodes(unittest.TestCase):

    def test__init__0(self):
        nodes = nodes_.Nodes()
        self.assertEqual(nodes.data, dict())

    def test__init__1(self):
        nodes = nodes_.Nodes(['n1', 'n2'])
        self.assertEqual(nodes.data, {'n1': None, 'n2': None})

    def test__init__2(self):
        nodes = nodes_.Nodes(['n1', 'n2', 'n1'])
        self.assertEqual(nodes.data, {'n1': None, 'n2': None})

    def test__init__3(self):
        nodes = nodes_.Nodes([('n1', 'N1'), ('n2', 'N2')])
        self.assertEqual(nodes.data, {('n1','N1'): None, ('n2','N2'): None})

    def test__init__3_data_true(self):
        nodes = nodes_.Nodes([('n1', 'N1'), ('n2', 'N2')], data=True)
        self.assertEqual(nodes.data, {'n1': 'N1', 'n2': 'N2'})

    def test__init__3_nodedata_true(self):
        nodes = nodes_.Nodes([('n1', 'N1'), ('n2', 'N2')], nodedata=True)
        self.assertEqual(nodes.data, {'n1': 'N1', 'n2': 'N2'})

    def test__init__3_nodedata_true_data_false(self):
        nodes = nodes_.Nodes([('n1', 'N1'), ('n2', 'N2')], nodedata=True, data=False)
        self.assertEqual(nodes.data, {'n1': 'N1', 'n2': 'N2'})

    def test__init__4(self):
        nodes = nodes_.Nodes({'n1': 'N1', 'n2': 'N2'})
        self.assertEqual(nodes.data, {'n1': 'N1', 'n2': 'N2'})

    def test__init__4_data_false(self):
        nodes = nodes_.Nodes({'n1': 'N1', 'n2': 'N2'}, data=False)
        self.assertEqual(nodes.data, {('n1','N1'): None, ('n2','N2'): None})

    def test__init__4_nodedata_false(self):
        nodes = nodes_.Nodes({'n1': 'N1', 'n2': 'N2'}, nodedata=False)
        self.assertEqual(nodes.data, {('n1','N1'): None, ('n2','N2'): None})

    def test__init__4_nodedata_false_data_true(self):
        nodes = nodes_.Nodes({'n1': 'N1', 'n2': 'N2'}, nodedata=False, data=True)
        self.assertEqual(nodes.data, {('n1','N1'): None, ('n2','N2'): None})

    def test__contains__(self):
        nodes = nodes_.Nodes({'n1': 'N1', 'n2': 'N2'})
        self.assertTrue('n1' in nodes)
        self.assertTrue('n2' in nodes)
        self.assertFalse('n3' in nodes)
        self.assertFalse('N1' in nodes)
        self.assertFalse('N2' in nodes)

    def test__iter__(self):
        nodes = nodes_.Nodes({'n1': 'N1', 'n2': 'N2'})
        self.assertEqual(list(iter(nodes)), list(nodes.data.keys()))

    def test__len__(self):
        nodes = nodes_.Nodes({'n1': 'N1', 'n2': 'N2'})
        self.assertEqual(len(nodes), 2)

    def test__repr__1(self):
        nodes = nodes_.Nodes({'n1': 'N1', 'n2': 'N2'})
        self.assertEqual(repr(nodes), "Nodes(%s)" % repr(nodes.data))

    def test__repr__2(self):
        nodes = nodes_.Nodes()
        self.assertEqual(repr(nodes), "Nodes()")

    def test__getitem__1(self):
        nodes = nodes_.Nodes({'n1': 'N1', 'n2': 'N2'})
        self.assertEqual(nodes['n1'],'N1')
        self.assertEqual(nodes['n2'],'N2')

    def test__getitem__2(self):
        nodes = nodes_.Nodes()
        with self.assertRaises(KeyError):
            nodes['x']

    def test__setitem__2(self):
        nodes = nodes_.Nodes({'n1':  'N1'})
        nodes['n1'] = '_N1_'
        nodes['n2'] = '_N2_'
        self.assertEqual(nodes.data, {'n1':  '_N1_', 'n2':  '_N2_'})

    def test__delitem__1(self):
        nodes = nodes_.Nodes({'n1': 'N1', 'n2': 'N2'})
        del nodes['n1']
        self.assertEqual(nodes.data, {'n2':  'N2'})

    def test__delitem__2(self):
        nodes = nodes_.Nodes({'n1': 'N1', 'n2': 'N2'})
        with self.assertRaises(KeyError):
            del nodes['n3']

    def test__add__1(self):
        nodes = nodes_.Nodes({'n1':  'N1'})
        nodes.add('n1', '_N1_')
        nodes.add('n2', '_N2_')
        self.assertEqual(nodes.data, {'n1':  '_N1_', 'n2':  '_N2_'})

    def test__add__2(self):
        nodes = nodes_.Nodes({'n1':  'N1'})
        nodes.add('n1')
        nodes.add('n2')
        self.assertEqual(nodes.data, {'n1':  'N1', 'n2':  None})

    def test__discard__1(self):
        nodes = nodes_.Nodes({'n1': 'N1', 'n2': 'N2'})
        nodes.discard('n1')
        self.assertEqual(nodes.data, {'n2':  'N2'})

    def test__discard__2(self):
        nodes = nodes_.Nodes({'n1': 'N1', 'n2': 'N2'})
        nodes.discard('n3')
        self.assertEqual(nodes.data, {'n1':  'N1', 'n2':  'N2'})

    def test__clear(self):
        nodes = nodes_.Nodes({'n1': 'N1', 'n2': 'N2'})
        nodes.clear()
        self.assertEqual(nodes.data, dict())

    def test__items(self):
        nodes = nodes_.Nodes({'n1': 'N1', 'n2': 'N2'})
        self.assertEqual(list(nodes.items()), list(nodes.data.items()))

if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
