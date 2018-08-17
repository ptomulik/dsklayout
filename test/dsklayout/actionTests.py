#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import dsklayout.action as action

class Test__action__PackageSymbols(unittest.TestCase):

    def test__action__symbols(self):
        self.assertIs(action.Action, action.action_.Action)

if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
