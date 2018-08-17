#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest

import dsklayout.graph.bfs_ as bfs_
import dsklayout.graph.traversal_ as traversal_
import dsklayout.graph.trail_ as trail_
import dsklayout.graph.graph_ as graph_

class Callbacks:

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
        return {'ingress_func':  self.ingress_func,
                'egress_func':  self.egress_func,
                'backedge_func':  self.backedge}


class Test__Bfs(unittest.TestCase):

    def graph1(self):
        nodes = ['p','q','r','s','t','u','v','x']
        edges = [('p','q'), ('p','r'), ('r','t'), ('t','u'), ('r','s'), ('s','p'), ('v','s')]
        return graph_.Graph(nodes, edges)

    def graph2(self):
        nodes = ['p','q','r','s','t','x']
        edges = [('p','q'), ('q','s'), ('r','p'), ('t','r')]
        return graph_.Graph(nodes, edges)

    def test__isinstance_Traversal(self):
        self.assertIsInstance(bfs_.Bfs(), traversal_.Traversal)

    def test__outward__1(self):
        cb = Callbacks()
        search = bfs_.Bfs(direction = 'outward', **cb.callbacks)
        trail = search(self.graph1(), ['p', 'x'])
        self.assertIsInstance(trail, trail_.Trail)
        self.assertIsNone(trail.result)
        self.assertEqual(trail.backedges, [('s','p')])

        self.assertIn(trail.nodes, [
            ['p','q','r','s','t','u','x'],
            ['p','q','r','t','s','u','x'],
            ['p','r','q','s','t','u','x'],
            ['p','r','q','t','s','u','x']
        ])

        if trail.nodes == ['p','q','r','s','t','u','x']:
            self.assertEqual(trail.edges, [('p','q'), ('p','r'), ('r','s'), ('r','t'), ('t','u')])
        elif trail.nodes == ['p','q','r','t','s','u','x']:
            self.assertEqual(trail.edges, [('p','q'), ('p','r'), ('r','t'), ('r','s'), ('t','u')])
        elif trail.nodes == ['p','r','q','s','t','u','x']:
            self.assertEqual(trail.edges, [('p','r'), ('p','q'), ('r','s'), ('r','t'), ('t','u')])
        elif trail.nodes == ['p','r','q','t','s','u','x']:
            self.assertEqual(trail.edges, [('p','r'), ('p','q'), ('r','t'), ('r','s'), ('t','u')])
        else:
            self.assertTrue(False) # fail
        self.assertEqual(cb.ingress_nodes, trail.nodes)
        self.assertEqual(cb.ingress_edges, trail.edges)
        self.assertEqual(cb.egress_nodes, trail.nodes)
        self.assertEqual(cb.egress_edges, trail.edges)
        self.assertEqual(cb.backedges, trail.backedges)

    def test__inward__1(self):
        cb = Callbacks()
        search = bfs_.Bfs(direction = 'inward', **cb.callbacks)
        trail = search(self.graph1(), ['p', 'x'])
        self.assertIsInstance(trail, trail_.Trail)
        self.assertIsNone(trail.result)
        self.assertEqual(trail.backedges, [('p','r')])

        self.assertIn(trail.nodes, [
            ['p','s','r','v','x'],
            ['p','s','v','r','x'],
        ])

        if trail.nodes == ['p','s','r','v','x']:
            self.assertEqual(trail.edges, [('s','p'), ('r','s'), ('v','s')])
        elif trail.nodes == ['p','s','v','r','x']:
            self.assertEqual(trail.edges, [('s','p'), ('v','s'), ('r','s')])
        else:
            self.assertTrue(False) # fail
        self.assertEqual(cb.ingress_nodes, trail.nodes)
        self.assertEqual(cb.ingress_edges, trail.edges)
        self.assertEqual(cb.egress_nodes, trail.nodes)
        self.assertEqual(cb.egress_edges, trail.edges)
        self.assertEqual(cb.backedges, trail.backedges)

    def test__incident__1(self):
        cb = Callbacks()
        search = bfs_.Bfs(direction = 'incident', **cb.callbacks)
        trail = search(self.graph2(), ['p', 'x'])
        self.assertIsInstance(trail, trail_.Trail)
        self.assertIsNone(trail.result)
        self.assertEqual(trail.backedges, [])

        self.assertIn(trail.nodes, [
            ['p', 'q', 'r', 's', 't', 'x'],
            ['p', 'r', 'q', 't', 's', 'x'],
        ])

        if trail.nodes == ['p', 'q', 'r', 's', 't', 'x']:
            self.assertEqual(trail.edges, [('p','q'), ('r','p'), ('q','s'), ('t','r')])
        elif trail.nodes == ['p', 'r', 'q', 't', 's', 'x']:
            self.assertEqual(trail.edges, [('r','p'), ('p','q'), ('t','r'), ('q','s')])
        else:
            self.assertTrue(False) # fail

        self.assertEqual(cb.ingress_nodes, trail.nodes)
        self.assertEqual(cb.ingress_edges, trail.edges)
        self.assertEqual(cb.egress_nodes, trail.nodes)
        self.assertEqual(cb.egress_edges, trail.edges)
        self.assertEqual(cb.backedges, trail.backedges)

    def test__stop_on_ingress(self):
        cb = Callbacks(ingress_func = lambda g,n,e: n == 's')
        self.stop_on_s_testfun(cb)

    def test__stop_on_egress(self):
        cb = Callbacks(egress_func = lambda g,n,e: n == 's')
        self.stop_on_s_testfun(cb)

    def stop_on_s_testfun(self, cb):
        search = bfs_.Bfs(direction = 'outward', **cb.callbacks)
        trail = search(self.graph1(), ['p', 'x'])
        self.assertIsInstance(trail, trail_.Trail)
        self.assertEqual(trail.result, 's')
        self.assertEqual(trail.backedges, [])

        self.assertIn(trail.nodes, [
            ['p','q','r','s'],
            ['p','q','r','t','s'],
            ['p','r','q','s'],
            ['p','r','q','t','s']
        ])

        if trail.nodes == ['p','q','r','s',]:
            self.assertEqual(trail.edges, [('p','q'), ('p','r'), ('r','s')])
        elif trail.nodes == ['p','q','r','t','s']:
            self.assertEqual(trail.edges, [('p','q'), ('p','r'), ('r','t'), ('r','s')])
        elif trail.nodes == ['p','r','q','s']:
            self.assertEqual(trail.edges, [('p','r'), ('p','q'), ('r','s')])
        elif trail.nodes == ['p','r','q','t','s']:
            self.assertEqual(trail.edges, [('p','r'), ('p','q'), ('r','t'), ('r','s')])
        else:
            self.assertTrue(False) # fail
        self.assertEqual(cb.ingress_nodes, trail.nodes)
        self.assertEqual(cb.ingress_edges, trail.edges)
        self.assertEqual(cb.egress_nodes, trail.nodes)
        self.assertEqual(cb.egress_edges, trail.edges)
        self.assertEqual(cb.backedges, trail.backedges)

    def test__stop_on_backedge(self):
        cb = Callbacks(backedge_func = lambda g,e: e == ('s','p'))
        search = bfs_.Bfs(direction = 'outward', **cb.callbacks)
        trail = search(self.graph1(), ['p', 'x'])
        self.assertIsInstance(trail, trail_.Trail)
        self.assertEqual(trail.result, ('s','p'))
        self.assertEqual(trail.backedges, [('s','p')])

        self.assertIn(trail.nodes, [
            ['p','q','r','s'],
            ['p','q','r','t','s'],
            ['p','r','q','s'],
            ['p','r','q','t','s']
        ])

        if trail.nodes == ['p','q','r','s',]:
            self.assertEqual(trail.edges, [('p','q'), ('p','r'), ('r','s')])
        elif trail.nodes == ['p','q','r','t','s']:
            self.assertEqual(trail.edges, [('p','q'), ('p','r'), ('r','t'), ('r','s')])
        elif trail.nodes == ['p','r','q','s']:
            self.assertEqual(trail.edges, [('p','r'), ('p','q'), ('r','s')])
        elif trail.nodes == ['p','r','q','t','s']:
            self.assertEqual(trail.edges, [('p','r'), ('p','q'), ('r','t'), ('r','s')])
        else:
            self.assertTrue(False) # fail
        self.assertEqual(cb.ingress_nodes, trail.nodes)
        self.assertEqual(cb.ingress_edges, trail.edges)
        self.assertEqual(cb.egress_nodes, trail.nodes)
        self.assertEqual(cb.egress_edges, trail.edges)
        self.assertEqual(cb.backedges, trail.backedges)

    def test__repeated_start_nodes_1(self):
        cb = Callbacks()
        graph = graph_.Graph(['p', 'q'], [('p', 'q')])
        search = bfs_.Bfs(direction = 'outward', **cb.callbacks)
        trail = search(graph, ['p', 'p'])
        self.assertEqual(trail.nodes, ['p', 'q'])
        self.assertEqual(trail.edges, [('p','q')])
        self.assertEqual(trail.backedges, [])
        self.assertEqual(cb.ingress_nodes, trail.nodes)
        self.assertEqual(cb.egress_nodes, trail.nodes)
        self.assertEqual(cb.ingress_edges, trail.edges)
        self.assertEqual(cb.egress_edges, trail.edges)
        self.assertEqual(cb.backedges, trail.backedges)


if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
