#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import unittest.mock as mock
import collections

import dsklayout.graph.trail_ as trail_

class Test__Trail(unittest.TestCase):

    def test__init__0(self):
        trail = trail_.Trail('graph')
        self.assertEqual(trail.graph, 'graph')
        self.assertEqual(trail.explored_nodes, set())
        self.assertEqual(trail.explored_edges, set())
        self.assertEqual(trail.nodes, list())
        self.assertEqual(trail.edges, list())
        self.assertEqual(trail.backedges, list())
        self.assertIsNone(trail.result)
        self.assertEqual(trail.queue, collections.deque())
        self.assertTrue(callable(trail.enter_func))
        self.assertTrue(callable(trail.leave_func))
        self.assertTrue(callable(trail.backedge_func))

    def test__nodes__1(self):
        trail = trail_.Trail('graph')
        trail.explore_node('p')
        trail.explore_node('q')
        self.assertEqual(trail.nodes, [])
        self.assertEqual(trail.explored_nodes, set(['p', 'q']))
        self.assertTrue(trail.node_explored('p'))
        self.assertTrue(trail.node_explored('q'))
        self.assertFalse(trail.node_explored('x'))

    def test__nodes__2(self):
        trail = trail_.Trail('graph')
        trail.append_node('p')
        trail.append_node('q')
        self.assertEqual(trail.nodes, ['p', 'q'])
        self.assertEqual(trail.explored_nodes, set())
        self.assertFalse(trail.node_explored('p'))
        self.assertFalse(trail.node_explored('q'))
        self.assertFalse(trail.node_explored('x'))

    def test__nodes__3(self):
        trail = trail_.Trail('graph')
        trail.explore_and_append_node('p')
        trail.explore_and_append_node('q')
        self.assertEqual(trail.nodes, ['p', 'q'])
        self.assertEqual(trail.explored_nodes, set(['p', 'q']))
        self.assertTrue(trail.node_explored('p'))
        self.assertTrue(trail.node_explored('q'))
        self.assertFalse(trail.node_explored('x'))

    def test__edges__1(self):
        trail = trail_.Trail('graph')
        trail.explore_edge(('p','q'))
        trail.explore_edge(('q','r'))
        trail.explore_edge(('r', 'p'))
        self.assertEqual(trail.edges, [])
        self.assertEqual(trail.backedges, [])
        self.assertEqual(trail.explored_edges, set([('p', 'q'), ('q', 'r'), ('r', 'p')]))
        self.assertTrue(trail.edge_explored(('p', 'q')))
        self.assertTrue(trail.edge_explored(('q', 'r')))
        self.assertTrue(trail.edge_explored(('r', 'p')))
        self.assertFalse(trail.edge_explored(('x','y')))

    def test__edges__2(self):
        trail = trail_.Trail('graph')
        trail.append_edge(('p','q'))
        trail.append_edge(('q','r'))
        trail.append_backedge(('r', 'p'))
        self.assertEqual(trail.edges, [('p', 'q'), ('q', 'r')])
        self.assertEqual(trail.backedges, [('r', 'p')])
        self.assertEqual(trail.explored_edges, set())
        self.assertFalse(trail.edge_explored(('p', 'q')))
        self.assertFalse(trail.edge_explored(('q', 'r')))
        self.assertFalse(trail.edge_explored(('r', 'p')))
        self.assertFalse(trail.edge_explored(('x','y')))

    def test__edges__3(self):
        trail = trail_.Trail('graph')
        trail.explore_and_append_edge(('p','q'))
        trail.explore_and_append_edge(('q','r'))
        trail.explore_and_append_backedge(('r', 'p'))
        self.assertEqual(trail.edges, [('p', 'q'), ('q', 'r')])
        self.assertEqual(trail.backedges, [('r', 'p')])
        self.assertEqual(trail.explored_edges, set([('p', 'q'), ('q', 'r'), ('r', 'p')]))
        self.assertTrue(trail.edge_explored(('p', 'q')))
        self.assertTrue(trail.edge_explored(('q', 'r')))
        self.assertTrue(trail.edge_explored(('r', 'p')))
        self.assertFalse(trail.edge_explored(('x','y')))

    def test__queue(self):
        trail = trail_.Trail('graph')
        trail.enqueue('p')
        trail.enqueue('q')
        self.assertEqual(trail.queue, collections.deque(['p', 'q']))
        self.assertFalse(trail.queue_empty())
        self.assertEqual(trail.dequeue(), 'p')
        self.assertEqual(trail.dequeue(), 'q')
        self.assertTrue(trail.queue_empty())

    def test__result(self):
        trail = trail_.Trail('graph')
        self.assertIsNone(trail.result)
        trail.result = 'result'
        self.assertEqual(trail.result, 'result')

    def test__callbacks(self):
        e,l,b = (lambda *args : False, lambda *args : False, lambda *args : False)
        trail = trail_.Trail('graph', enter_func=e, leave_func=l, backedge_func=b)
        self.assertIs(trail.enter_func, e)
        self.assertIs(trail.leave_func, l)
        self.assertIs(trail.backedge_func, b)


if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
