#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest

import dsklayout.model.exceptions_ as exceptions_

class Test__InconsistentDataError(unittest.TestCase):

    def test__base(self):
        self.assertIsInstance(exceptions_.InconsistentDataError(), Exception)

    def test__str(self):
        self.assertEqual(str(exceptions_.InconsistentDataError("foo bar")), "foo bar")

if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
