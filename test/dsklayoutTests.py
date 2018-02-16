#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import types
import dsklayout

class Test__dsklayout__PackageSymbols(unittest.TestCase):

    def test__graph__symbol(self):
        self.assertIsInstance(dsklayout.graph, types.ModuleType)

    def test__model__symbol(self):
        self.assertIsInstance(dsklayout.model, types.ModuleType)

    def test__model__symbol(self):
        self.assertIsInstance(dsklayout.util, types.ModuleType)

if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
