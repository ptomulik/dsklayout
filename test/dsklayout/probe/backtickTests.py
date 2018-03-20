#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import dsklayout.probe.backtick_ as backtick_
import dsklayout.probe.probe_ as probe_

class Test__BackTickProbe(unittest.TestCase):

    def test__subclass__1(self):
        self.assertTrue(issubclass(backtick_.BackTickProbe, probe_.Probe))

    def test__abstract__1(self):

        with self.assertRaises(TypeError) as context:
            backtick_.BackTickProbe()

        self.assertIn("abstract", str(context.exception))

    def test__derived__1(self):
        class T(backtick_.BackTickProbe):
            @classmethod
            def command(cls, **kw):
                return super().command(**kw)
            @classmethod
            def parse(cls, output):
                return super().parse(output)
            @classmethod
            def flags(cls, flags=None, **kw):
                return super().flags(flags, **kw)

        self.assertIsNone(T.command())
        self.assertIsNone(T.parse("output"))
        self.assertEqual(T.flags(), [])


if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
