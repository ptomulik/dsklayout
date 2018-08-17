#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest

import dsklayout.util as util

class Test__util__PackageSymbols(unittest.TestCase):

    def test__dispatch__symbols(self):
        self.assertIs(util.dispatch, util.dispatch_.dispatch)

    def test__imports__symbols(self):
        self.assertIs(util.import_all_from, util.imports_.import_all_from)
        self.assertIs(util.import_from, util.imports_.import_from)

    def test__misc__symbols(self):
        self.assertIs(util.add_dict_getters, util.misc_.add_dict_getters)

    def test__subprocess__symbols(self):
        self.assertIs(util.backtick, util.subprocess_.backtick)


if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
