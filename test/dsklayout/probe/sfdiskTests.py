#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
from unittest.mock import patch
import os.path
import json

import dsklayout.probe.sfdisk_ as sfdisk_

backtick = 'dsklayout.util.backtick'

class Test__Sfdisk(unittest.TestCase):

    def test__content(self):
        content = 'content'
        sfdisk = sfdisk_.Sfdisk(content)
        self.assertIs(sfdisk.content, content)

    def test__run__with_no_args(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(sfdisk_.Sfdisk.run(), 'ok')
            mock.assert_called_once_with(['sfdisk', '-J'])

    def test__run__with_device(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(sfdisk_.Sfdisk.run('sda'), 'ok')
            mock.assert_called_once_with(['sfdisk', '-J', 'sda'])

    def test__run__with_devices(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(sfdisk_.Sfdisk.run(['sda', 'sdb']), 'ok')
            mock.assert_called_once_with(['sfdisk', '-J', 'sda', 'sdb'])

    def test__run__with_devices_and_flags(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(sfdisk_.Sfdisk.run(['sda', 'sdb'], ['-x', '-y']), 'ok')
            mock.assert_called_once_with(['sfdisk', '-J', '-x', '-y',  'sda', 'sdb'])

    def test__run__with_custom_sfdisk(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(sfdisk_.Sfdisk.run(['sda', 'sdb'], ['-x', '-y'], sfdisk='/opt/bin/sfdisk'), 'ok')
            mock.assert_called_once_with(['/opt/bin/sfdisk', '-J', '-x', '-y',  'sda', 'sdb'])

    def test__new__with_no_args(self):
        with patch(backtick, return_value='{"foo":"bar"}') as mock:
            sfdisk = sfdisk_.Sfdisk.new()
            self.assertIsInstance(sfdisk, sfdisk_.Sfdisk)
            self.assertEqual(sfdisk.content, {"foo":  "bar"})
            mock.assert_called_once_with(['sfdisk', '-J'])

    def test__new__with_device(self):
        with patch(backtick, return_value='{"foo":"bar"}') as mock:
            sfdisk = sfdisk_.Sfdisk.new('sda')
            self.assertIsInstance(sfdisk, sfdisk_.Sfdisk)
            self.assertEqual(sfdisk.content, {"foo":  "bar"})
            mock.assert_called_once_with(['sfdisk', '-J', 'sda'])

    def test__new__with_devices(self):
        with patch(backtick, return_value='{"foo":"bar"}') as mock:
            sfdisk = sfdisk_.Sfdisk.new(['sda', 'sdb'])
            self.assertIsInstance(sfdisk, sfdisk_.Sfdisk)
            self.assertEqual(sfdisk.content, {"foo":  "bar"})
            mock.assert_called_once_with(['sfdisk', '-J', 'sda', 'sdb'])

    def test__new__with_devices_and_flags(self):
        with patch(backtick, return_value='{"foo":"bar"}') as mock:
            sfdisk = sfdisk_.Sfdisk.new(['sda', 'sdb'], ['-x', '-y'])
            self.assertIsInstance(sfdisk, sfdisk_.Sfdisk)
            self.assertEqual(sfdisk.content, {"foo":  "bar"})
            mock.assert_called_once_with(['sfdisk', '-J', '-x', '-y',  'sda', 'sdb'])

    def test__new__with_custom_sfdisk(self):
        with patch(backtick, return_value='{"foo":"bar"}') as mock:
            sfdisk = sfdisk_.Sfdisk.new(['sda', 'sdb'], ['-x', '-y'], sfdisk='/opt/bin/sfdisk')
            self.assertIsInstance(sfdisk, sfdisk_.Sfdisk)
            self.assertEqual(sfdisk.content, {"foo":  "bar"})
            mock.assert_called_once_with(['/opt/bin/sfdisk', '-J', '-x', '-y',  'sda', 'sdb'])


if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
