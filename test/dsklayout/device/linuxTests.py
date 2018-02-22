#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import unittest.mock as mock

import dsklayout.device.linux_ as linux_
import dsklayout.device.device_ as device_
import dsklayout.model.lsblkdev_ as lsblkdev_


class Test__LinuxDevice(unittest.TestCase):

    def test__issubclass__Device(self):
        self.assertTrue(issubclass(linux_.LinuxDevice, device_.Device))

    def test__init__1(self):
        dev = linux_.LinuxDevice('foo')
        self.assertEqual(dev.properties, 'foo')

    def test__specargs__1(self):
        with self.assertRaises(TypeError) as context:
            linux_.LinuxDevice.specargs('foo')
        self.assertEqual("LinuxDevice.specargs() can't take str as argument", str(context.exception))

    def test__specargs__2(self):
        dev = lsblkdev_.LsBlkDev({'name': '/dev/sda'})
        args = linux_.LinuxDevice.specargs(dev)
        self.assertEqual(args, (dev.properties,))

    def test__supports__1(self):
        self.assertFalse(linux_.LinuxDevice.supports('foo'))

    def test__supports__2(self):
        dev = lsblkdev_.LsBlkDev({'name': '/dev/sda'})
        self.assertEqual(linux_.LinuxDevice.supports(dev), 1)

if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
