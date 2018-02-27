#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import dsklayout.tool as tool

class Test__tool__PackageSymbols(unittest.TestCase):

    def test__backtick__symbols(self):
        self.assertIs(tool.BackTick, tool.backtick_.BackTick)

    def test__fdisk__symbols(self):
        self.assertIs(tool.Fdisk, tool.fdisk_.Fdisk)

    def test__lsblk__symbols(self):
        self.assertIs(tool.LsBlk, tool.lsblk_.LsBlk)

if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
