#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import dsklayout.probe as probe

class Test__probe__PackageSymbols(unittest.TestCase):

    def test__backtick__symbols(self):
        self.assertIs(probe.BackTick, probe.backtick_.BackTick)

    def test__fdisk__symbols(self):
        self.assertIs(probe.Fdisk, probe.fdisk_.Fdisk)

    def test__lsblk__symbols(self):
        self.assertIs(probe.LsBlk, probe.lsblk_.LsBlk)

    def test__sfdisk__symbols(self):
        self.assertIs(probe.Sfdisk, probe.sfdisk_.Sfdisk)

if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
