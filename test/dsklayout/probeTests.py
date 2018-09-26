#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import dsklayout.probe as probe

class Test__probe__PackageSymbols(unittest.TestCase):

    def test__backtick__symbols(self):
        self.assertIs(probe.BackTickProbe, probe.backtick_.BackTickProbe)

    def test__composite__symbols(self):
        self.assertIs(probe.CompositeProbe, probe.composite_.CompositeProbe)

    def test__fdisk__symbols(self):
        self.assertIs(probe.FdiskProbe, probe.fdisk_.FdiskProbe)

    def test__fdiskparser__symbols(self):
        self.assertIs(probe.FdiskParser, probe.fdiskparser_.FdiskParser)

    def test__lsblk__symbols(self):
        self.assertIs(probe.LsBlkProbe, probe.lsblk_.LsBlkProbe)

    def test__sfdisk__symbols(self):
        self.assertIs(probe.SfdiskProbe, probe.sfdisk_.SfdiskProbe)

    def test__lvm__symbols(self):
        self.assertIs(probe.LvsProbe, probe.lvm_.LvsProbe)
        self.assertIs(probe.VgsProbe, probe.lvm_.VgsProbe)
        self.assertIs(probe.PvsProbe, probe.lvm_.PvsProbe)
        self.assertIs(probe.LvmProbe, probe.lvm_.LvmProbe)

    def test__mdadm__symbols(self):
        self.assertIs(probe.MdadmDetailProbe, probe.mdadm_.MdadmDetailProbe)
        self.assertIs(probe.MdadmExamineProbe, probe.mdadm_.MdadmExamineProbe)
        self.assertIs(probe.MdadmProbe, probe.mdadm_.MdadmProbe)

if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
