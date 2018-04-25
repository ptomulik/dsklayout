#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import unittest.mock as mock

import dsklayout.cli.ext_ as ext_
import dsklayout.cli.cmdbase_ as cmdbase_

class TestCliExt(ext_.CliExt):
    @property
    def name(self):
        return 'test'

class Test__CliExt(unittest.TestCase):

    def test__isinstance__CmdBase(self):
        ext = TestCliExt()
        self.assertIsInstance(ext, cmdbase_.CmdBase)

    def test__parent__AttributeError(self):
        ext = TestCliExt()
        with self.assertRaises(AttributeError) as context:
            ext.parent
        self.assertEqual('_parent', str(context.exception))

    def test__parent__setter(self):
        ext = TestCliExt()
        parent = mock.Mock()
        ext.parent = parent
        self.assertIs(ext.parent, parent)
        self.assertIs(ext._parent, parent)

    def test__arguments__AttributeError(self):
        ext = TestCliExt()
        with self.assertRaises(AttributeError) as context:
            ext.arguments
        self.assertEqual('_parent', str(context.exception))

    def test__arguments__setter(self):
        ext = TestCliExt()
        arguments = mock.Mock()
        with self.assertRaises(AttributeError) as context:
            ext.arguments = arguments
        self.assertEqual("can't set attribute", str(context.exception))

    def test__arguments__with_parent(self):
        ext = TestCliExt()
        parent = mock.Mock('parent')
        parent.arguments = mock.Mock('arguments')
        ext.parent = parent
        self.assertIs(ext.arguments, parent.arguments)

    def test__add_arguments(self):
        ext = TestCliExt()
        parser = mock.Mock(spec = [])
        self.assertIsNone(ext.add_arguments(parser))

    def test__set_defaults(self):
        ext = TestCliExt()
        parser = mock.Mock(spec = [])
        self.assertIsNone(ext.set_defaults(parser))


if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
