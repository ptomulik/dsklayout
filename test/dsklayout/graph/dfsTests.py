#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest

import dsklayout.graph.dfs_ as dfs_
import dsklayout.graph.traversal_ as traversal_
import dsklayout.graph.trail_ as trail_
import dsklayout.graph.graph_ as graph_

class Callbacks(object):

    def __init__(self, **kw):
        self.ingress_nodes = list()
        self.ingress_edges = list()
        self.egress_nodes = list()
        self.egress_edges = list()
        self.backedges = list()
        self._ingress_func = kw.get('ingress_func', lambda g,n,e: False)
        self._egress_func = kw.get('egress_func', lambda g,n,e: False)
        self._backedge_func = kw.get('backedge_func', lambda g,e: False)

    def ingress_func(self, graph, node, edge):
        self.ingress_nodes.append(node)
        if edge is not None: self.ingress_edges.append(edge)
        return (self._ingress_func)(graph, node, edge)

    def egress_func(self, graph, node, edge):
        self.egress_nodes.append(node)
        if edge is not None: self.egress_edges.append(edge)
        return (self._egress_func)(graph, node, edge)

    def backedge(self, graph, edge):
        self.backedges.append(edge)
        return (self._backedge_func)(graph, edge)

    @property
    def callbacks(self):
        return { 'ingress_func' : self.ingress_func,
                 'egress_func' : self.egress_func,
                 'backedge_func' : self.backedge }


class Test__Dfs(unittest.TestCase):

    def graph1(self):
        nodes = [ 'p','q','r','s','x' ]
        edges = [ ('p','q'), ('q','r'), ('q','s'), ('s','p') ]
        return graph_.Graph(nodes, edges)

    def graph2(self):
        nodes = [ 'p','q','r','s','t','u','x' ]
        edges = [ ('p','q'), ('q','r'), ('q','s'), ('s', 'p'), ('s', 't'), ('r','u') ]
        return graph_.Graph(nodes, edges)

    def test__isinstance_Traversal(self):
        self.assertIsInstance(dfs_.Dfs(), traversal_.Traversal)

    def test__outward__1(self):
        cb = Callbacks()
        search = dfs_.Dfs(direction = 'outward', **cb.callbacks)
        trail = search(self.graph1(), ['p', 'x'])
        self.assertIsInstance(trail, trail_.Trail)
        self.assertIsNone(trail.result)
        self.assertEqual(trail.backedges, [('s','p')])
        self.assertIn(trail.nodes, [['p','q','r','s','x'], ['p','q','s','r','x']])
        if trail.nodes == ['p','q','r','s','x']:
            self.assertEqual(trail.edges, [('p','q'), ('q','r'), ('q','s')])
            self.assertEqual(cb.egress_nodes, ['r','s','q','p','x'])
            self.assertEqual(cb.egress_edges, [('q','r'), ('q','s'), ('p','q')])
        else:
            self.assertEqual(trail.edges, [('p','q'), ('q','s'), ('q','r')])
            self.assertEqual(cb.egress_nodes, ['s','r','q','p','x'])
            self.assertEqual(cb.egress_edges, [('q','s'), ('q','r'), ('p','q')])
        self.assertEqual(cb.ingress_edges, trail.edges)
        self.assertEqual(cb.ingress_nodes, trail.nodes)
        self.assertEqual(cb.backedges, trail.backedges)

    def test__inward__1(self):
        cb = Callbacks()
        search = dfs_.Dfs(direction = 'inward', **cb.callbacks)
        trail = search(self.graph1(), ['p', 'x'])
        self.assertIsInstance(trail, trail_.Trail)
        self.assertIsNone(trail.result)
        self.assertEqual(trail.nodes, ['p','s','q','x'])
        self.assertEqual(trail.edges, [('s','p'), ('q','s')])
        self.assertEqual(trail.backedges, [('p','q')])
        self.assertEqual(cb.ingress_edges, trail.edges)
        self.assertEqual(cb.ingress_nodes, trail.nodes)
        self.assertEqual(cb.egress_nodes, ['q','s','p','x'])
        self.assertEqual(cb.egress_edges, [('q','s'),('s','p')])
        self.assertEqual(cb.backedges, trail.backedges)

    def test__incident__1(self):
        cb = Callbacks()
        search = dfs_.Dfs(direction = 'incident', **cb.callbacks)
        trail = search(self.graph1(), ['p', 'x'])
        self.assertIsInstance(trail, trail_.Trail)
        self.assertIsNone(trail.result)
        self.assertIn(trail.backedges, [[('p','q')], [('s','p')]])
        if trail.backedges == [('s','p')]:
            self.assertIn(trail.nodes, [['p','q','r','s','x'], ['p','q','s','r','x']])
            if trail.nodes == ['p','q','r','s','x']:
                self.assertEqual(cb.egress_nodes, ['r','s','q','p','x'])
                self.assertEqual(cb.egress_edges, [('q','r'), ('q','s'), ('p','q')])
            else:
                self.assertEqual(cb.egress_nodes, ['s','r','q','p','x'])
                self.assertEqual(cb.egress_edges, [('q','s'), ('q','r'), ('p','q')])
        else:
            self.assertEqual(trail.nodes, ['p','s','q','r','x'])
        self.assertEqual(cb.ingress_edges, trail.edges)
        self.assertEqual(cb.ingress_nodes, trail.nodes)
        self.assertEqual(cb.backedges, trail.backedges)

    def test__stop_on_ingress(self):
        cb = Callbacks(ingress_func = lambda g,n,e: n == 's')
        search = dfs_.Dfs(direction = 'outward', **cb.callbacks)
        trail = search(self.graph1(), ['p', 'x'])
        self.assertIsInstance(trail, trail_.Trail)
        self.assertEqual(trail.result, 's')
        self.assertEqual(trail.backedges, [])
        self.assertIn(trail.nodes, [['p','q','r','s'],['p','q','s']]) # 'x' is never visited
        if trail.nodes == ['p','q','r','s']:
            self.assertEqual(trail.edges, [('p','q'), ('q','r'), ('q','s')])
            self.assertEqual(cb.egress_nodes, ['r', 's', 'q', 'p'])
            self.assertEqual(cb.egress_edges, [('q','r'), ('q','s'), ('p','q')])
        else:
            self.assertEqual(trail.edges, [('p','q'), ('q','s')])
            self.assertEqual(cb.egress_nodes, ['s', 'q', 'p'])
            self.assertEqual(cb.egress_edges, [('q','s'), ('p','q')])
        self.assertEqual(cb.ingress_nodes, trail.nodes)
        self.assertEqual(cb.ingress_edges, trail.edges)
        self.assertEqual(cb.backedges, trail.backedges)

    def test__stop_on_egress(self):
        cb = Callbacks(egress_func = lambda g,n,e: n == 'r')
        search = dfs_.Dfs(direction = 'outward', **cb.callbacks)
        trail = search(self.graph2(), ['p', 'x'])
        self.assertIsInstance(trail, trail_.Trail)
        self.assertEqual(trail.result, 'r')
        self.assertIn(trail.backedges, [[('s','p')],[]])
        if trail.backedges == []:
            self.assertEqual(trail.nodes, ['p', 'q', 'r', 'u'])
            self.assertEqual(trail.edges, [('p', 'q'), ('q', 'r'), ('r','u')])
            self.assertEqual(cb.egress_nodes, ['u', 'r', 'q', 'p'])
            self.assertEqual(cb.egress_edges, [('r','u'), ('q','r'), ('p','q')])
        else:
            self.assertEqual(trail.nodes, ['p', 'q', 's', 't', 'r', 'u'])
            self.assertEqual(trail.edges, [('p', 'q'), ('q','s'), ('s','t'), ('q', 'r'), ('r','u')])
            self.assertEqual(cb.egress_nodes, ['t', 's', 'u', 'r', 'q', 'p'])
            self.assertEqual(cb.egress_edges, [('s','t'), ('q','s'), ('r','u'), ('q','r'), ('p','q')])
        self.assertEqual(cb.ingress_nodes, trail.nodes)
        self.assertEqual(cb.ingress_edges, trail.edges)
        self.assertEqual(cb.backedges, trail.backedges)

    def test__stop_on_backedge(self):
        cb = Callbacks(backedge_func = lambda g,e: e == ('s','p'))
        search = dfs_.Dfs(direction = 'outward', **cb.callbacks)
        trail = search(self.graph2(), ['p','x'])
        self.assertIsInstance(trail, trail_.Trail)
        self.assertEqual(trail.result, ('s','p'))
        self.assertEqual(trail.backedges,[('s','p')])
        if 't' in trail.nodes:
            self.assertIn(trail.nodes, [['p','q','r','u','s','t'], ['p','q','s','t']])
            if trail.nodes == ['p','q','r','u','s','t']:
                self.assertEqual(trail.edges, [('p','q'), ('q','r'), ('r','u'), ('q','s'), ('s','t')])
                self.assertEqual(cb.egress_nodes, ['u','r','t','s','q','p'])
                self.assertEqual(cb.egress_edges, [('r','u'), ('q','r'), ('s','t'), ('q','s'), ('p','q')])
            else:
                self.assertEqual(trail.edges, [('p','q'), ('q','s'), ('s','t')])
                self.assertEqual(cb.egress_nodes, ['t','s','q','p'])
                self.assertEqual(cb.egress_edges, [('s','t'), ('q','s'), ('p','q')])
        else:
            self.assertIn(trail.nodes, [['p','q','r','u','s'], ['p','q','s']])
            if trail.nodes == ['p','q','r','u','s']:
                self.assertEqual(trail.edges, [('p','q'), ('q','r'), ('r','u'), ('q','s')])
                self.assertEqual(cb.egress_nodes, ['u','r','s','q','p'])
                self.assertEqual(cb.egress_edges, [('r','u'), ('q','r'), ('q','s'), ('p','q')])
            else:
                self.assertEqual(trail.edges, [('p','q'), ('q','s')])
                self.assertEqual(cb.egress_nodes, ['s','q','p'])
                self.assertEqual(cb.egress_edges, [('q','s'), ('p','q')])
        self.assertEqual(cb.ingress_nodes, trail.nodes)
        self.assertEqual(cb.ingress_edges, trail.edges)
        self.assertEqual(cb.backedges, trail.backedges)

    def test__repeated_start_nodes_1(self):
        cb = Callbacks()
        graph = graph_.Graph(['p', 'q'], [('p', 'q')])
        search = dfs_.Dfs(direction = 'outward', **cb.callbacks)
        trail = search(graph, ['p', 'p'])
        self.assertEqual(trail.nodes, ['p', 'q'])
        self.assertEqual(trail.edges, [('p','q')])
        self.assertEqual(trail.backedges, [])
        self.assertEqual(cb.ingress_nodes, ['p', 'q'])
        self.assertEqual(cb.egress_nodes, ['q', 'p'])
        self.assertEqual(cb.ingress_edges, [('p','q')])
        self.assertEqual(cb.egress_edges, [('p','q')])
        self.assertEqual(cb.backedges, [])

if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
