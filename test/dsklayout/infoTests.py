#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import dsklayout.info as info

class Test__info__PackageSymbols(unittest.TestCase):

    def test__backtick__symbols(self):
        self.assertIs(info.BackTick, info.backtick_.BackTick)

    def test__fdisk__symbols(self):
        self.assertIs(info.Fdisk, info.fdisk_.Fdisk)

    def test__lsblk__symbols(self):
        self.assertIs(info.LsBlk, info.lsblk_.LsBlk)

if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
