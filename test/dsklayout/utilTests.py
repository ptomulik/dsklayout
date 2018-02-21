#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest

import dsklayout.util as util

class Test__util__PackageSymbols(unittest.TestCase):

    def test__imports__symbols(self):
        self.assertIs(util.import_all_from, util.imports_.import_all_from)
        self.assertIs(util.import_from, util.imports_.import_from)

    def test__subprocess__symbols(self):
        self.assertIs(util.backtick, util.subprocess_.backtick)

    def test__dispatch__symbols(self):
        self.assertIs(util.dispatch, util.dispatch_.dispatch)

if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
