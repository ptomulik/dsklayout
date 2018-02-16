#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import dsklayout.graph as graph

class Test__dsklayout_graph__PackageSymbols(unittest.TestCase):

    def test__bfs__symbols(self):
        self.assertIs(graph.Bfs, graph.bfs_.Bfs)

    def test__dfs__symbols(self):
        self.assertIs(graph.Dfs, graph.dfs_.Dfs)

    def test__edges__symbols(self):
        self.assertIs(graph.Edges, graph.edges_.Edges)

    def test__elems__symbols(self):
        self.assertIs(graph.Elems, graph.elems_.Elems)

    def test__exceptions__symbols(self):
        self.assertTrue(True)

    def test__graph__symbols(self):
        self.assertIs(graph.Graph, graph.graph_.Graph)

    def test__nodes__symbols(self):
        self.assertIs(graph.Nodes, graph.nodes_.Nodes)

    def test__trail__symbols(self):
        self.assertIs(graph.Trail, graph.trail_.Trail)

    def test__traversal__symbols(self):
        self.assertIs(graph.Traversal, graph.traversal_.Traversal)

if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
