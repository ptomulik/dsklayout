#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import unittest.mock as mock

import dsklayout.device.linuxdisk_ as linuxdisk_
import dsklayout.device.linux_ as linux_
import dsklayout.model.lsblkdev_ as lsblkdev_


class Test__LinuxDisk(unittest.TestCase):

    def test__issubclass__LinuxDevice(self):
        self.assertTrue(issubclass(linuxdisk_.LinuxDisk, linux_.LinuxDevice))

    def test__init__1(self):
        dev = linuxdisk_.LinuxDisk('foo')
        self.assertEqual(dev.properties, 'foo')

    def test__specargs__1(self):
        with self.assertRaises(TypeError) as context:
            linuxdisk_.LinuxDisk.specargs('foo')
        self.assertEqual("LinuxDevice.specargs() can't take str as argument", str(context.exception))

    def test__specargs__2(self):
        dev = lsblkdev_.LsBlkDev({'name': '/dev/sda'})
        args = linuxdisk_.LinuxDisk.specargs(dev)
        self.assertEqual(args, (dev.properties,))

    def test__supports__1(self):
        self.assertFalse(linuxdisk_.LinuxDisk.supports('foo'))

    def test__supports__2(self):
        dev = lsblkdev_.LsBlkDev({'name': '/dev/sda'})
        self.assertFalse(linuxdisk_.LinuxDisk.supports(dev))

    def test__supports__3(self):
        dev = lsblkdev_.LsBlkDev({'name': '/dev/sda', 'type': 'disk'})
        self.assertEqual(linuxdisk_.LinuxDisk.supports(dev), 2)


if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
