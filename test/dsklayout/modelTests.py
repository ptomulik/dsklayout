#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import dsklayout.model as model

class Test__model__PackageSymbols(unittest.TestCase):

    def test__backtick__symbols(self):
        self.assertIs(model.BackTick, model.backtick_.BackTick)

    def test__fdisk__symbols(self):
        self.assertIs(model.Fdisk, model.fdisk_.Fdisk)

    def test__lsblk__symbols(self):
        self.assertIs(model.LsBlk, model.lsblk_.LsBlk)

    def test__lsblkdev__symbols(self):
        self.assertIs(model.LsBlkDev, model.lsblkdev_.LsBlkDev)

    def test__exceptions__symbols(self):
        self.assertIs(model.InconsistentDataError, model.exceptions_.InconsistentDataError)

if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
