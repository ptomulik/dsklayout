#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import dsklayout.probe as probe

class Test__probe__PackageSymbols(unittest.TestCase):

    def test__backtick__symbols(self):
        self.assertIs(probe.BackTickProbe, probe.backtick_.BackTickProbe)

    def test__fdisk__symbols(self):
        self.assertIs(probe.FdiskProbe, probe.fdisk_.FdiskProbe)

    def test__lsblk__symbols(self):
        self.assertIs(probe.LsBlkProbe, probe.lsblk_.LsBlkProbe)

    def test__sfdisk__symbols(self):
        self.assertIs(probe.SfdiskProbe, probe.sfdisk_.SfdiskProbe)

if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
