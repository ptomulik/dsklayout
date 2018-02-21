#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
from unittest.mock import patch
import types

import dsklayout.util.subprocess_ as subprocess_

class Test__Backtick(unittest.TestCase):

    def test__backtick__with_two_args(self):
        def side(cmd, **kw):
            return 'ok'
        with patch('subprocess.PIPE') as pipe, \
             patch('subprocess.check_output') as check_output:

            check_output.side_effect = side
            self.assertIs(subprocess_.backtick('cmd', 'input', 'timeout'), 'ok')
            check_output.assert_called_once_with('cmd', stdin=pipe,
                                                        stderr=pipe,
                                                        universal_newlines=True,
                                                        timeout='timeout')

    def test__backtick__with_one_arg(self):
        def side(cmd, **kw):
            return 'ok'
        with patch('subprocess.PIPE') as pipe, \
             patch('subprocess.check_output') as check_output:

            check_output.side_effect = side
            self.assertIs(subprocess_.backtick('cmd', 'input'), 'ok')
            check_output.assert_called_once_with('cmd', stdin=pipe,
                                                        stderr=pipe,
                                                        universal_newlines=True,
                                                        timeout=None)

    def test__backtick__with_no_args(self):
        def side(cmd, **kw):
            return 'ok'
        with patch('subprocess.PIPE') as pipe, \
             patch('subprocess.check_output') as check_output:

            check_output.side_effect = side
            self.assertIs(subprocess_.backtick('cmd'), 'ok')
            check_output.assert_called_once_with('cmd', stdin=None,
                                                        stderr=pipe,
                                                        universal_newlines=True,
                                                        timeout=None)


if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
