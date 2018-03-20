#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import dsklayout.device as device


class Test__device__PackageSymbols(unittest.TestCase):

    def test__device__symbols(self):
        self.assertIs(device.Device, device.device_.Device)

    def test__linuxdevice__symbols(self):
        self.assertIs(device.LinuxDevice, device.linuxdevice_.LinuxDevice)

    def test__partitiontable__symbols(self):
        self.assertIs(device.PartitionTable, device.partitiontable_.PartitionTable)

    def test__partition__symbols(self):
        self.assertIs(device.Partition, device.partition_.Partition)

if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
