#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import unittest.mock as mock

import dsklayout.device.device_ as device_
import dsklayout.util as util


class Test__Device(unittest.TestCase):

    def test__is_abstract(self):
        with self.assertRaises(TypeError) as context:
            device_.Device()
        self.assertIn('abstract', str(context.exception))

    def test__new__01(self):
        with self.assertRaises(util.FactoryError) as context:
            device_.Device.new('foo')
        self.assertEqual("can't create Device from %r" % 'foo', str(context.exception))

    def test__subclass__01(self):
        class D(device_.Device):
            @classmethod
            def supports(cls, spec):
                return super().supports(spec)

        d = D()
        self.assertIsNone(d.supports('foo'))


if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
