#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import unittest.mock as mock

import dsklayout.cli.cmd_ as cmd_
import dsklayout.cli.cmdbase_ as cmdbase_

class TestCmd(cmd_.Cmd):
    @property
    def name(self):
        return 'test'

class Test__Cmd(unittest.TestCase):

    def extMock(self, name=None):
        if name is None:
            ext = mock.Mock('NoNameExt')
        else:
            ext = mock.Mock('%sExt' % name)
            ext.name = name
        ext.add_arguments = mock.Mock('add_arguments')
        ext.set_defaults = mock.Mock('set_defaults')
        return ext

    def test__isinstance_cmdbase(self):
        cmd = TestCmd()
        self.assertIsInstance(cmd, cmdbase_.CmdBase)

    def test__init__0(self):
        cmd = TestCmd()
        self.assertEqual(cmd.extensions, dict())
        with self.assertRaises(AttributeError):
            cmd.arguments

    def test__AttributeError(self):
        cmd = TestCmd()
        with self.assertRaises(AttributeError) as context:
            cmd.foo
        self.assertEqual('foo', str(context.exception))

    def test__arguments__AttributeError(self):
        cmd = TestCmd()
        with self.assertRaises(AttributeError) as context:
            cmd.arguments
        self.assertEqual('arguments', str(context.exception))

    def test__properties(self):
        cmd = TestCmd()
        self.assertEqual(cmd.properties, dict())

    def test__arguments__setter(self):
        cmd = TestCmd()
        args = mock.Mock()
        cmd.arguments = args
        self.assertIs(cmd.arguments, args)
        self.assertIs(cmd._arguments, args)

    def test__properties__setter_AttributeError(self):
        cmd = TestCmd()
        with self.assertRaises(AttributeError) as context:
            cmd.properties = 'foo'
        self.assertEqual("can't set attribute", str(context.exception))

    def test__add_extension__custom_name(self):
        cmd = TestCmd()
        ext = self.extMock()
        cmd.add_extension(ext, 'foo')
        self.assertIn('foo', cmd.extensions)
        self.assertIs(cmd.extensions['foo'], ext)
        self.assertIs(ext.parent, cmd)
        self.assertIs(cmd.foo, ext)

    def test__add_extension__ext_name(self):
        cmd = TestCmd()
        ext = self.extMock('foo')
        cmd.add_extension(ext)
        self.assertIn('foo', cmd.extensions)
        self.assertIs(cmd.extensions['foo'], ext)
        self.assertIs(ext.parent, cmd)
        self.assertIs(cmd.foo, ext)

    def test__add_extension__AttributeError(self):
        cmd = TestCmd()
        ext = self.extMock()
        with self.assertRaises(AttributeError) as context:
            cmd.add_extension(ext)
        self.assertIn('name', str(context.exception))

    def test__add_arguments(self):
        parser = mock.Mock(spec=[])
        with mock.patch.object(TestCmd,'add_cmd_arguments') as add_cmd_arguments, \
             mock.patch.object(TestCmd,'add_ext_arguments') as add_ext_arguments:
                cmd = TestCmd()
                self.assertIsNone(cmd.add_arguments(parser))
                add_cmd_arguments.assert_called_once_with(parser)
                add_ext_arguments.assert_called_once_with(parser)

    def test__set_defaults(self):
        parser = mock.Mock(spec=[])
        with mock.patch.object(TestCmd,'set_cmd_defaults') as set_cmd_defaults, \
             mock.patch.object(TestCmd,'set_ext_defaults') as set_ext_defaults:
                cmd = TestCmd()
                self.assertIsNone(cmd.set_defaults(parser))
                set_cmd_defaults.assert_called_once_with(parser)
                set_ext_defaults.assert_called_once_with(parser)

    def test__add_cmd_arguments(self):
        cmd = TestCmd()
        parser = mock.Mock(spec =[])
        self.assertIsNone(cmd.add_cmd_arguments(parser))

    def test__set_cmd_defaults(self):
        cmd = TestCmd()
        parser = mock.Mock(spec =[])
        self.assertIsNone(cmd.set_cmd_defaults(parser))

    def test__set_cmd_defaults(self):
        cmd = TestCmd()
        parser = mock.Mock(spec =[])
        self.assertIsNone(cmd.set_cmd_defaults(parser))

    def test__add_ext_arguments(self):
        cmd = TestCmd()
        parser = mock.Mock(spec =[])
        ext1, ext2 = (mock.Mock(spec=['add_arguments']), mock.Mock(spec=['add_arguments']))
        cmd.add_extension(ext1, 'ext1')
        cmd.add_extension(ext2, 'ext2')
        self.assertIsNone(cmd.add_ext_arguments(parser))
        ext1.add_arguments.assert_called_once_with(parser)
        ext2.add_arguments.assert_called_once_with(parser)

    def test__set_ext_defaults(self):
        cmd = TestCmd()
        parser = mock.Mock(spec =[])
        ext1, ext2 = (mock.Mock(spec=['set_defaults']), mock.Mock(spec=['set_defaults']))
        cmd.add_extension(ext1, 'ext1')
        cmd.add_extension(ext2, 'ext2')
        self.assertIsNone(cmd.set_ext_defaults(parser))
        ext1.set_defaults.assert_called_once_with(parser)
        ext2.set_defaults.assert_called_once_with(parser)

    def test__run(self):
        self.assertEqual(TestCmd().run(), 0)

if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
