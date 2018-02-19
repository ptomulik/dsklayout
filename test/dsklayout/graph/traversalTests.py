#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import unittest.mock as mock

import dsklayout.graph.traversal_ as traversal_

class Traversal(traversal_.Traversal):
    def __call__(self, graph, startpoint, *args, **kw):
        super().__call__(graph, startpoint, *args, **kw)


class Test__Traversal(unittest.TestCase):

    def test__init__0(self):
        traversal = Traversal()
        self.assertEqual(traversal.edge_selector, traversal.select_incident_edges)
        self.assertTrue(callable(traversal.enter_func))
        self.assertTrue(callable(traversal.leave_func))
        self.assertTrue(callable(traversal.backedge_func))

    def test__init__1(self):
        edge_selector = lambda g,n: ()
        enter_func = lambda *args: False
        leave_func = lambda *args: False
        backedge_func = lambda *args: False
        traversal = Traversal( edge_selector = edge_selector,
                               enter_func    = enter_func,
                               leave_func    = leave_func,
                               backedge_func= backedge_func )
        self.assertIs(traversal.edge_selector, edge_selector)
        self.assertIs(traversal.enter_func, enter_func)
        self.assertIs(traversal.leave_func, leave_func)
        self.assertIs(traversal.backedge_func, backedge_func)

    def test__init__2(self):
        edge_selector = lambda g,n: ()
        traversal = Traversal( direction = edge_selector )
        self.assertIs(traversal.edge_selector, edge_selector)

    def test__edge_selector__setter_1(self):
        edge_selector = lambda g,n: ()
        traversal = Traversal(edge_selector = edge_selector)
        traversal.edge_selector = None
        self.assertEqual(traversal.edge_selector, traversal.select_incident_edges)

    def test__edge_selector__setter_2(self):
        edge_selector = lambda g,n: ()
        traversal = Traversal()
        traversal.edge_selector = edge_selector
        self.assertIs(traversal.edge_selector, edge_selector)

    def test__edge_selector__setter_3(self):
        edge_selector = lambda g,n: ()
        traversal = Traversal()
        traversal.edge_selector = 'both'
        self.assertEqual(traversal.edge_selector, traversal.select_both_edges)

    def test__edge_selector__setter_4(self):
        edge_selector = lambda g,n: ()
        traversal = Traversal()
        traversal.edge_selector = 'incident'
        self.assertEqual(traversal.edge_selector, traversal.select_incident_edges)

    def test__edge_selector__setter_5(self):
        edge_selector = lambda g,n: ()
        traversal = Traversal()
        traversal.edge_selector = 'inward'
        self.assertEqual(traversal.edge_selector, traversal.select_inward_edges)

    def test__edge_selector__setter_6(self):
        edge_selector = lambda g,n: ()
        traversal = Traversal()
        traversal.edge_selector = 'outward'
        self.assertEqual(traversal.edge_selector, traversal.select_outward_edges)

    def test__edge_selector__setter_ValueError(self):
        edge_selector = lambda g,n: ()
        traversal = Traversal()
        with self.assertRaises(ValueError) as context:
            traversal.edge_selector = 'abc'
        self.assertEqual("Invalid edge selector %s" % repr('abc'), str(context.exception))

    def test__enter_func__setter_1(self):
        enter_func = lambda *args: False
        traversal = Traversal()
        traversal.enter_func = enter_func
        self.assertIs(traversal.enter_func, enter_func)

    def test__enter_func__setter_TypeError(self):
        enter_func = lambda *args: False
        traversal = Traversal()
        with self.assertRaises(TypeError) as context:
            traversal.enter_func = 123
        self.assertEqual("enter_func must be callable, int provided", str(context.exception))

    def test__leave_func__setter_1(self):
        leave_func = lambda *args: False
        traversal = Traversal()
        traversal.leave_func = leave_func
        self.assertIs(traversal.leave_func, leave_func)

    def test__leave_func__setter_TypeError(self):
        leave_func = lambda *args: False
        traversal = Traversal()
        with self.assertRaises(TypeError) as context:
            traversal.leave_func = 123
        self.assertEqual("leave_func must be callable, int provided", str(context.exception))

    def test__backedge_func__setter_1(self):
        backedge_func = lambda *args: False
        traversal = Traversal()
        traversal.backedge_func = backedge_func
        self.assertIs(traversal.backedge_func, backedge_func)

    def test__backedge_func__setter_TypeError(self):
        backedge_func = lambda *args: False
        traversal = Traversal()
        with self.assertRaises(TypeError) as context:
            traversal.backedge_func = 123
        self.assertEqual("backedge_func must be callable, int provided", str(context.exception))

    def test__select_edges(self):
        edge_selector = mock.Mock(return_value='ok')
        traversal = Traversal(edge_selector = edge_selector)
        self.assertEqual(traversal.select_edges('g', 'n'), 'ok')
        edge_selector.assert_called_once_with('g','n')

    def test__select_incident_edges(self):
        graph = mock.Mock()
        graph.incident = mock.Mock(return_value = 'ok')
        traversal = Traversal()
        self.assertEqual(traversal.select_incident_edges(graph, 'n'), 'ok')
        graph.incident.assert_called_once_with('n')

    def test__select_both_edges(self):
        graph = mock.Mock()
        graph.incident = mock.Mock(return_value = 'ok')
        traversal = Traversal()
        self.assertEqual(traversal.select_both_edges(graph, 'n'), 'ok')
        graph.incident.assert_called_once_with('n')

    def test__select_inward_edges(self):
        graph = mock.Mock()
        graph.inward = mock.Mock(return_value = 'ok')
        traversal = Traversal()
        self.assertEqual(traversal.select_inward_edges(graph, 'n'), 'ok')
        graph.inward.assert_called_once_with('n')

    def test__select_outward_edges(self):
        graph = mock.Mock()
        graph.outward = mock.Mock(return_value = 'ok')
        traversal = Traversal()
        self.assertEqual(traversal.select_outward_edges(graph, 'n'), 'ok')
        graph.outward.assert_called_once_with('n')


    def test__call__(self):
        self.assertIsNone(Traversal()('graph', 'startpoint'))

if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
