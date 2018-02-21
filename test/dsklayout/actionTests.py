#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import dsklayout.action as action

class Test__action__PackageSymbols(unittest.TestCase):

    def test__action__symbols(self):
        self.assertIs(action.Action, action.action_.Action)

    def test__subject__symbols(self):
        self.assertIs(action.ActionSubject, action.subject_.ActionSubject)

if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
