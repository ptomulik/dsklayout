#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import unittest.mock as mock

import dsklayout.cli.cmdbase_ as cmdbase_

class TestCmd(cmdbase_.CliCmdBase):
    @property
    def name(self):
        return 'test'
    def parent_name(self):
        return super().name

class Test__CliCmdBase(unittest.TestCase):

    def test__is_abstract(self):
        with self.assertRaises(TypeError) as context:
            cmd = cmdbase_.CliCmdBase()
        self.assertIn('abstract', str(context.exception))

    def test__name(self):
        cmd = TestCmd()
        self.assertIsNone(cmd.parent_name())

    def test__add_aruments(self):
        parser = mock.Mock(spec = [])
        cmd = TestCmd()
        self.assertIsNone(cmd.add_arguments(parser))

    def test__set_defauls(self):
        parser = mock.Mock(spec = [])
        cmd = TestCmd()
        self.assertIsNone(cmd.set_defaults(parser))




if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
