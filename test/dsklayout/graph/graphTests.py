#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest

import dsklayout.graph.graph_ as graph_
import dsklayout.graph.edges_ as edges_
import dsklayout.graph.nodes_ as nodes_

class Test__Graph(unittest.TestCase):

    def test__init__0(self):
        graph = graph_.Graph()
        self.assertEqual(graph.edges, edges_.Edges())
        self.assertEqual(graph.nodes, nodes_.Nodes())

    def test__init__1(self):
        graph = graph_.Graph(['p', 'q', 'r', 's'],[('p','q'), ('q','r')])
        self.assertIsInstance(graph.nodes, nodes_.Nodes)
        self.assertEqual(graph.nodes.data, {'p':  None, 'q':  None, 'r':  None, 's':  None})
        self.assertIsInstance(graph.edges, edges_.Edges)
        self.assertEqual(graph.edges.data, {('p','q'):  None, ('q','r'):  None})

    def test__init__2(self):
        graph = graph_.Graph({'p':'P', 'q':'Q', 'r':'R'}, {('p','q'):'1', ('q','r'):'2'})
        self.assertIsInstance(graph.nodes, nodes_.Nodes)
        self.assertEqual(graph.nodes.data, {'p':  'P', 'q':  'Q', 'r':  'R'})
        self.assertIsInstance(graph.edges, edges_.Edges)
        self.assertEqual(graph.edges.data, {('p','q'):'1', ('q','r'):'2'})

    def test__init__inconsistent_1(self):
        with self.assertRaises(KeyError) as context:
            graph_.Graph(['p', 'q'], [('p','q'), ('q','r')])
        self.assertEqual(repr('r'), str(context.exception))

    def test__init__inconsistent_2(self):
        with self.assertRaises(KeyError) as context:
            graph_.Graph(['q', 'r'], [('p','q'), ('q','r')])
        self.assertEqual(repr('p'), str(context.exception))

    def test__init__consistency_false(self):
        graph = graph_.Graph(['p', 'q'], [('p','q'), ('q','r')], consistency=False)
        self.assertIsInstance(graph.nodes, nodes_.Nodes)
        self.assertEqual(graph.nodes.data, {'p':  None, 'q':  None})
        self.assertIsInstance(graph.edges, edges_.Edges)
        self.assertEqual(graph.edges.data, {('p','q'):  None, ('q','r'):  None})

    def test__repr__(self):
        graph = graph_.Graph(['p', 'q', 'r'], [('p','q'), ('q','r')])
        self.assertEqual(repr(graph), "Graph(%s, %s)" % (repr(graph.nodes),repr(graph.edges)))

    def test__add_node__1(self):
        graph = graph_.Graph({'p':'P', 'q':'Q', 'r':'R'}, {('p','q'):'1', ('q','r'):'2'})
        graph.add_node('r')
        self.assertEqual(graph.nodes.data, {'p':'P', 'q':'Q', 'r':'R'})
        self.assertEqual(graph.edges.data, {('p','q'):'1', ('q','r'):'2'})

    def test__add_node__2(self):
        graph = graph_.Graph({'p':'P', 'q':'Q', 'r':'R'}, {('p','q'):'1', ('q','r'):'2'})
        graph.add_node('r',None)
        self.assertEqual(graph.nodes.data, {'p':'P', 'q':'Q', 'r':None})
        self.assertEqual(graph.edges.data, {('p','q'):'1', ('q','r'):'2'})

    def test__add_node__3(self):
        graph = graph_.Graph({'p':'P', 'q':'Q', 'r':'R'}, {('p','q'):'1', ('q','r'):'2'})
        graph.add_node('s')
        self.assertEqual(graph.nodes.data, {'p':'P', 'q':'Q', 'r':'R', 's':None})
        self.assertEqual(graph.edges.data, {('p','q'):'1', ('q','r'):'2'})

    def test__add_node__4(self):
        graph = graph_.Graph({'p':'P', 'q':'Q', 'r':'R'}, {('p','q'):'1', ('q','r'):'2'})
        graph.add_node('s','S')
        self.assertEqual(graph.nodes.data, {'p':'P', 'q':'Q', 'r':'R', 's':'S'})
        self.assertEqual(graph.edges.data, {('p','q'):'1', ('q','r'):'2'})

    def test__del_node__1(self):
        graph = graph_.Graph({'p':'P', 'q':'Q', 'r':'R'}, {('p','q'):'1', ('q','r'):'2'})
        graph.del_node('p')
        self.assertEqual(graph.nodes.data, {'q':'Q', 'r':'R'})
        self.assertEqual(graph.edges.data, {('q','r'):'2'})

    def test__del_node__2(self):
        graph = graph_.Graph({'p':'P', 'q':'Q', 'r':'R'}, {('p','q'):'1', ('q','r'):'2'})
        graph.del_node('q')
        self.assertEqual(graph.nodes.data, {'p':'P', 'r':'R'})
        self.assertEqual(graph.edges.data, dict())

    def test__del_node__KeyError(self):
        graph = graph_.Graph()
        with self.assertRaises(KeyError) as context:
            graph.del_node('x')
        self.assertEqual(repr('x'), str(context.exception))

    def test__discard_node__1(self):
        graph = graph_.Graph({'p':'P', 'q':'Q', 'r':'R'}, {('p','q'):'1', ('q','r'):'2'})
        graph.discard_node('p')
        self.assertEqual(graph.nodes.data, {'q':'Q', 'r':'R'})
        self.assertEqual(graph.edges.data, {('q','r'):'2'})

    def test__discard_node__2(self):
        graph = graph_.Graph({'p':'P', 'q':'Q', 'r':'R'}, {('p','q'):'1', ('q','r'):'2'})
        graph.discard_node('q')
        self.assertEqual(graph.nodes.data, {'p':'P', 'r':'R'})
        self.assertEqual(graph.edges.data, dict())

    def test__discard_node__3(self):
        graph = graph_.Graph({'p':'P', 'q':'Q', 'r':'R'}, {('p','q'):'1', ('q','r'):'2'})
        graph.discard_node('x')
        self.assertEqual(graph.nodes.data, {'p':'P', 'q':'Q', 'r':'R'})
        self.assertEqual(graph.edges.data, {('p','q'):'1', ('q','r'):'2'})

    def test__has_node(self):
        graph = graph_.Graph({'p':'P', 'q':'Q', 'r':'R'})
        self.assertTrue(graph.has_node('p'))
        self.assertTrue(graph.has_node('q'))
        self.assertTrue(graph.has_node('r'))
        self.assertFalse(graph.has_node('x'))

    def test__node__1(self):
        graph = graph_.Graph({'p':'P', 'q':'Q', 'r':'R'})
        self.assertEqual(graph.node('p'), 'P')
        self.assertEqual(graph.node('q'), 'Q')
        self.assertEqual(graph.node('r'), 'R')

    def test__node__2(self):
        graph = graph_.Graph(['p', 'q', 'r'])
        self.assertIsNone(graph.node('p'))
        self.assertIsNone(graph.node('q'))
        self.assertIsNone(graph.node('r'))

    def test__node__KeyError(self):
        graph = graph_.Graph(['p', 'q', 'r'])
        with self.assertRaises(KeyError) as context:
            graph.node('x')
        self.assertEqual(repr('x'), str(context.exception))

    def test__add_edge__1(self):
        graph = graph_.Graph({'p':'P', 'q':'Q', 'r':'R'}, {('p','q'):'1', ('q','r'):'2'})
        graph.add_edge(('p','r'))
        self.assertEqual(graph.nodes.data, {'p':'P', 'q':'Q', 'r':'R'})
        self.assertEqual(graph.edges.data, {('p','q'):'1', ('q','r'):'2', ('p','r'):None})

    def test__add_edge__2(self):
        graph = graph_.Graph({'p':'P', 'q':'Q', 'r':'R'}, {('p','q'):'1', ('q','r'):'2'})
        graph.add_edge(('p','r'), '3')
        self.assertEqual(graph.nodes.data, {'p':'P', 'q':'Q', 'r':'R'})
        self.assertEqual(graph.edges.data, {('p','q'):'1', ('q','r'):'2', ('p','r'):'3'})

    def test__add_edge__3(self):
        graph = graph_.Graph({'p':'P', 'q':'Q'}, {('p','q'):'1'})
        graph.add_edge(('q','r'), '2')
        self.assertEqual(graph.nodes.data, {'p':'P', 'q':'Q', 'r':None})
        self.assertEqual(graph.edges.data, {('p','q'):'1', ('q','r'):'2'})

    def test__add_edge__4(self):
        graph = graph_.Graph({'p':'P', 'q':'Q'}, {('p','q'):'1'})
        graph.add_edge(('q','r'), '2', r='R')
        self.assertEqual(graph.nodes.data, {'p':'P', 'q':'Q', 'r':'R'})
        self.assertEqual(graph.edges.data, {('p','q'):'1', ('q','r'):'2'})

    def test__add_edge__ValueError_1(self):
        graph = graph_.Graph({'p':'P', 'q':'Q'}, {('p','q'):'1'})
        with self.assertRaises(ValueError) as context:
            graph.add_edge(('q',))
##        self.assertIn('not enough values to unpack', str(context.exception))

    def test__add_edge__ValueError_2(self):
        graph = graph_.Graph({'p':'P', 'q':'Q'}, {('p','q'):'1'})
        with self.assertRaises(ValueError) as context:
            graph.add_edge(('q','r','s'))
##        self.assertIn('too many values to unpack', str(context.exception))

    def test__del_edge(self):
        graph = graph_.Graph({'p':'P', 'q':'Q', 'r':'R'}, {('p','q'):'1', ('q','r'):'2'})
        graph.del_edge(('q','r'))
        self.assertEqual(graph.nodes.data, {'p':'P', 'q':'Q', 'r':'R'})
        self.assertEqual(graph.edges.data, {('p','q'):'1'})

    def test__del_edge__KeyError(self):
        graph = graph_.Graph({'p':'P', 'q':'Q', 'r':'R'}, {('p','q'):'1', ('q','r'):'2'})
        with self.assertRaises(KeyError) as context:
            graph.del_edge(('p','r'))
        self.assertEqual(repr(('p','r')), str(context.exception))
        self.assertEqual(graph.nodes.data, {'p':'P', 'q':'Q', 'r':'R'})
        self.assertEqual(graph.edges.data, {('p','q'):'1', ('q','r'):'2'})

    def test__discard_edge__1(self):
        graph = graph_.Graph({'p':'P', 'q':'Q', 'r':'R'}, {('p','q'):'1', ('q','r'):'2'})
        graph.discard_edge(('q','r'))
        self.assertEqual(graph.nodes.data, {'p':'P', 'q':'Q', 'r':'R'})
        self.assertEqual(graph.edges.data, {('p','q'):'1'})

    def test__discard_edge__2(self):
        graph = graph_.Graph({'p':'P', 'q':'Q', 'r':'R'}, {('p','q'):'1', ('q','r'):'2'})
        graph.discard_edge(('p','r')) # must not throw
        self.assertEqual(graph.nodes.data, {'p':'P', 'q':'Q', 'r':'R'})
        self.assertEqual(graph.edges.data, {('p','q'):'1', ('q','r'):'2'})

    def test__has_edge__1(self):
        graph = graph_.Graph({'p':'P', 'q':'Q', 'r':'R'}, {('p','q'):'1', ('q','r'):'2'})
        self.assertTrue(graph.has_edge(('p','q')))
        self.assertTrue(graph.has_edge(('q','r')))

    def test__has_edge__2(self):
        graph = graph_.Graph({'p':'P', 'q':'Q', 'r':'R'}, {('p','q'):'1', ('q','r'):'2'})
        self.assertFalse(graph.has_edge(('q','p')))
        self.assertFalse(graph.has_edge(('r','q')))
        self.assertFalse(graph.has_edge(('p','r')))
        self.assertFalse(graph.has_edge(('r','p')))

    def test__has_edge__3(self):
        graph = graph_.Graph({'p':'P', 'q':'Q', 'r':'R'}, {('p','q'):'1', ('q','r'):'2'})
        self.assertFalse(graph.has_edge(('x','y')))
        self.assertFalse(graph.has_edge(('x',)))
        self.assertFalse(graph.has_edge(('x','y','z')))

    def test__edge__1(self):
        graph = graph_.Graph(['p', 'q', 'r'], {('p','q'):'1', ('q','r'):'2'})
        self.assertEqual(graph.edge(('p','q')), '1')
        self.assertEqual(graph.edge(('q','r')), '2')

    def test__edge__2(self):
        graph = graph_.Graph(['p', 'q', 'r'], [('p','q'), ('q','r')])
        self.assertIsNone(graph.edge(('p','q')))
        self.assertIsNone(graph.edge(('q','r')))

    def test__edge__KeyError(self):
        graph = graph_.Graph(['p', 'q', 'r'], [('p','q'), ('q','r')])
        with self.assertRaises(KeyError) as context:
            graph.edge(('x','y'))
        self.assertEqual(repr(('x','y')), str(context.exception))

    def test__has_successors(self):
        graph = graph_.Graph(['p','q','r','s','t'], [('p','q'), ('q','r'), ('q','s')])
        self.assertTrue(graph.has_successors('p'))
        self.assertTrue(graph.has_successors('q'))
        self.assertFalse(graph.has_successors('r'))
        self.assertFalse(graph.has_successors('t'))

    def test__has_predecessors(self):
        graph = graph_.Graph(['p','q','r','s','t'], [('p','q'), ('q','r'), ('s','r')])
        self.assertFalse(graph.has_predecessors('p'))
        self.assertTrue(graph.has_predecessors('q'))
        self.assertTrue(graph.has_predecessors('r'))
        self.assertFalse(graph.has_predecessors('s'))
        self.assertFalse(graph.has_predecessors('t'))

    def test__has_neighbors(self):
        graph = graph_.Graph(['p','q','r','s','t'], [('p','q'), ('q','r'), ('s','r')])
        self.assertTrue(graph.has_neighbors('p'))
        self.assertTrue(graph.has_neighbors('q'))
        self.assertTrue(graph.has_neighbors('r'))
        self.assertTrue(graph.has_neighbors('s'))
        self.assertFalse(graph.has_neighbors('t'))

    def test__successors__1(self):
        graph = graph_.Graph(['p','q'], [('p','q')])
        self.assertEqual(type(graph.successors('p')), set)

    def test__successors__2(self):
        graph = graph_.Graph(['p','q','r','s','t'], [('p','q'), ('q','r'), ('q','s')])
        self.assertEqual(graph.successors('p'), set(['q',]))
        self.assertEqual(graph.successors('q'), set(['r','s']))
        self.assertEqual(graph.successors('r'), set())
        self.assertEqual(graph.successors('t'), set()) # isolated node, must not throw

    def test__successors__KeyError(self):
        graph = graph_.Graph(['p','q'], [('p','q')])
        with self.assertRaises(KeyError) as context:
            graph.successors('x')
        self.assertEqual(repr('x'), str(context.exception))

    def test__predecessors__1(self):
        graph = graph_.Graph(['p','q'], [('p','q')])
        self.assertEqual(type(graph.predecessors('p')), set)

    def test__predecessors__2(self):
        graph = graph_.Graph(['p','q','r','s','t'], [('p','q'), ('q','r'), ('s','r')])
        self.assertEqual(graph.predecessors('p'), set())
        self.assertEqual(graph.predecessors('q'), set(['p',]))
        self.assertEqual(graph.predecessors('r'), set(['q','s']))
        self.assertEqual(graph.predecessors('s'), set())
        self.assertEqual(graph.predecessors('t'), set()) # isolated node, must not throw

    def test__predecessors__KeyError(self):
        graph = graph_.Graph(['p','q'], [('p','q')])
        with self.assertRaises(KeyError) as context:
            graph.predecessors('x')
        self.assertEqual(repr('x'), str(context.exception))

    def test__neighbors__1(self):
        graph = graph_.Graph(['p','q'], [('p','q')])
        self.assertEqual(type(graph.neighbors('p')), set)

    def test__neighbors__2(self):
        graph = graph_.Graph(['p','q','r','s','t'], [('p','q'), ('q','r'), ('s','r')])
        self.assertEqual(graph.neighbors('p'), set(['q']))
        self.assertEqual(graph.neighbors('q'), set(['p','r']))
        self.assertEqual(graph.neighbors('r'), set(['q','s']))
        self.assertEqual(graph.neighbors('s'), set(['r']))
        self.assertEqual(graph.neighbors('t'), set()) # isolated node, must not throw

    def test__neighbors__KeyError(self):
        graph = graph_.Graph(['p','q'], [('p','q')])
        with self.assertRaises(KeyError) as context:
            graph.neighbors('x')
        self.assertEqual(repr('x'), str(context.exception))

    def test__outward__1(self):
        graph = graph_.Graph(['p','q'], [('p','q')])
        self.assertEqual(type(graph.outward('p')), set)

    def test__outward__2(self):
        graph = graph_.Graph(['p','q','r','s','t'], [('p','q'), ('p','r'), ('s','r')])
        self.assertEqual(graph.outward('p'), set([('p','q'), ('p','r')]))
        self.assertEqual(graph.outward('q'), set())
        self.assertEqual(graph.outward('r'), set())
        self.assertEqual(graph.outward('s'), set([('s','r')]))
        self.assertEqual(graph.outward('t'), set()) # isolated node, must not throw

    def test__outward__KeyError(self):
        graph = graph_.Graph(['p','q'], [('p','q')])
        with self.assertRaises(KeyError) as context:
            graph.outward('x')
        self.assertEqual(repr('x'), str(context.exception))

    def test__inward__1(self):
        graph = graph_.Graph(['p','q'], [('p','q')])
        self.assertEqual(type(graph.inward('q')), set)

    def test__inward__2(self):
        graph = graph_.Graph(['p','q','r','s','t'], [('p','q'), ('p','r'), ('s','r')])
        self.assertEqual(graph.inward('p'), set())
        self.assertEqual(graph.inward('q'), set([('p','q')]))
        self.assertEqual(graph.inward('r'), set([('p','r'),('s','r')]))
        self.assertEqual(graph.inward('s'), set())
        self.assertEqual(graph.inward('t'), set()) # isolated node, must not throw

    def test__inward__KeyError(self):
        graph = graph_.Graph(['p','q'], [('p','q')])
        with self.assertRaises(KeyError) as context:
            graph.inward('x')
        self.assertEqual(repr('x'), str(context.exception))

    def test__incident__1(self):
        graph = graph_.Graph(['p','q'], [('p','q')])
        self.assertEqual(type(graph.incident('q')), set)

    def test__incident__2(self):
        graph = graph_.Graph(['p','q','r','s','t'], [('p','q'), ('p','r'), ('s','r')])
        self.assertEqual(graph.incident('p'), set([('p','q'), ('p','r')]))
        self.assertEqual(graph.incident('q'), set([('p','q')]))
        self.assertEqual(graph.incident('r'), set([('p','r'),('s','r')]))
        self.assertEqual(graph.incident('s'), set([('s','r')]))
        self.assertEqual(graph.incident('t'), set()) # isolated node, must not throw

    def test__incident__KeyError(self):
        graph = graph_.Graph(['p','q'], [('p','q')])
        with self.assertRaises(KeyError) as context:
            graph.incident('x')
        self.assertEqual(repr('x'), str(context.exception))

    def test__adjacent__1(self):
        self.assertEqual(graph_.Graph.adjacent('p',('p','q')), 'q')
        self.assertEqual(graph_.Graph.adjacent('q',('p','q')), 'p')

    def test__adjacent__KeyError(self):
        with self.assertRaises(KeyError) as context:
            graph_.Graph.adjacent('x', ('p','q'))
        self.assertEqual(repr('x'), str(context.exception))

    def test__roots(self):
        graph = graph_.Graph(['p','q','r','s','t'], [('p','q'), ('p','r'), ('s','r')])
        self.assertEqual(graph.roots(), set(['p','s','t']))

    def test__leafs(self):
        graph = graph_.Graph(['p','q','r','s','t'], [('p','q'), ('p','r'), ('s','r')])
        self.assertEqual(graph.leafs(), set(['q','r','t']))

    def test__isolated(self):
        graph = graph_.Graph(['p','q','r','s','t'], [('p','q'), ('p','r'), ('s','r')])
        self.assertEqual(graph.isolated(), set(['t']))

if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
