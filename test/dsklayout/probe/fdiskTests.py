#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
from unittest.mock import patch
import os
import os.path
import json

import dsklayout.probe.fdisk_ as fdisk_

backtick = 'dsklayout.util.backtick'

class Test__Fdisk(unittest.TestCase):

    fixture_plan = [
        ('fdisk_1_sda_sdb.txt',    'fdisk_1_sda_sdb.content.json'),
        ('fdisk_1_sda.txt',        'fdisk_1_sda.content.json'),
        ('fdisk_2_sda_sdb.txt',    'fdisk_2_sda_sdb.content.json'),
    ]

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._fixtures = dict()

    def tearDown(self):
        self._fixtures = dict() # cleanup used fixtures

    @property
    def fixtures(self):
        if not self._fixtures:
            self.load_fixtures()
        return self._fixtures

    def load_fixtures(self):
        for left, right in self.fixture_plan:
            with open(self.fixture_path(left)) as f:
                self._fixtures[left] = f.read()
            with open(self.fixture_path(right)) as f:
                self._fixtures[right] = json.loads(f.read())

    def fixture_path(self, file):
        mydir = os.path.dirname(__file__)
        return os.path.join(mydir, 'fixtures', file)

    def test__content(self):
        content = 'content'
        fdisk = fdisk_.FdiskProbe(content)
        self.assertIs(fdisk.content, content)

    def test__run__with_no_args(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(fdisk_.FdiskProbe.run(env=dict()), 'ok')
            mock.assert_called_once_with(['fdisk', '-l', '--bytes'], env={'LC_NUMERIC': 'C'})

    def test__run__with_device(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(fdisk_.FdiskProbe.run('sda', env=dict()), 'ok')
            mock.assert_called_once_with(['fdisk', '-l', '--bytes', 'sda'], env={'LC_NUMERIC': 'C'})

    def test__run__with_devices(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(fdisk_.FdiskProbe.run(['sda', 'sdb'], env=dict()), 'ok')
            mock.assert_called_once_with(['fdisk', '-l', '--bytes', 'sda', 'sdb'], env={'LC_NUMERIC': 'C'})

    def test__run__with_devices_and_flags(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(fdisk_.FdiskProbe.run(['sda', 'sdb'], ['-x', '-y'], env=dict()), 'ok')
            mock.assert_called_once_with(['fdisk', '-l', '--bytes', '-x', '-y',  'sda', 'sdb'], env={'LC_NUMERIC': 'C'})

    def test__run__with_custom_fdisk(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(fdisk_.FdiskProbe.run(['sda', 'sdb'], ['-x', '-y'], fdisk='/opt/bin/fdisk', env=dict()), 'ok')
            mock.assert_called_once_with(['/opt/bin/fdisk', '-l', '--bytes', '-x', '-y',  'sda', 'sdb'], env={'LC_NUMERIC': 'C'})

    def test__new__with_no_args(self):
        with patch(backtick, return_value='Disk /dev/sda: 931.5 GiB, 1000204886016 bytes, 1953525168 sectors') as mock:
            fdisk = fdisk_.FdiskProbe.new(env=dict())
            self.assertIsInstance(fdisk, fdisk_.FdiskProbe)
            self.assertEqual(fdisk.content, [{"name":  "/dev/sda", "size": "931.5 GiB", "bytes": 1000204886016, "sectors": 1953525168}])
            mock.assert_called_once_with(['fdisk', '-l', '--bytes'], env={'LC_NUMERIC': 'C'})

    def test__new__with_device(self):
        with patch(backtick, return_value='Disk /dev/sda: 931.5 GiB, 1000204886016 bytes, 1953525168 sectors') as mock:
            fdisk = fdisk_.FdiskProbe.new('sda', env=dict())
            self.assertIsInstance(fdisk, fdisk_.FdiskProbe)
            self.assertEqual(fdisk.content, [{"name":  "/dev/sda", "size": "931.5 GiB", "bytes": 1000204886016, "sectors": 1953525168}])
            mock.assert_called_once_with(['fdisk', '-l', '--bytes', 'sda'], env={'LC_NUMERIC': 'C'})

    def test__new__with_devices(self):
        with patch(backtick, return_value='Disk /dev/sda: 931.5 GiB, 1000204886016 bytes, 1953525168 sectors') as mock:
            fdisk = fdisk_.FdiskProbe.new(['sda', 'sdb'], env=dict())
            self.assertIsInstance(fdisk, fdisk_.FdiskProbe)
            self.assertEqual(fdisk.content, [{"name":  "/dev/sda", "size": "931.5 GiB", "bytes": 1000204886016, "sectors": 1953525168}])
            mock.assert_called_once_with(['fdisk', '-l', '--bytes', 'sda', 'sdb'], env={'LC_NUMERIC': 'C'})

    def test__new__with_devices_and_flags(self):
        with patch(backtick, return_value='Disk /dev/sda: 931.5 GiB, 1000204886016 bytes, 1953525168 sectors') as mock:
            fdisk = fdisk_.FdiskProbe.new(['sda', 'sdb'], ['-x', '-y'], env=dict())
            self.assertIsInstance(fdisk, fdisk_.FdiskProbe)
            self.assertEqual(fdisk.content, [{"name":  "/dev/sda", "size": "931.5 GiB", "bytes": 1000204886016, "sectors": 1953525168}])
            mock.assert_called_once_with(['fdisk', '-l', '--bytes', '-x', '-y',  'sda', 'sdb'], env={'LC_NUMERIC': 'C'})

    def test__new__with_custom_fdisk(self):
        with patch(backtick, return_value='Disk /dev/sda: 931.5 GiB, 1000204886016 bytes, 1953525168 sectors') as mock:
            fdisk = fdisk_.FdiskProbe.new(['sda', 'sdb'], ['-x', '-y'], fdisk='/opt/bin/fdisk', env=dict())
            self.assertIsInstance(fdisk, fdisk_.FdiskProbe)
            self.assertEqual(fdisk.content, [{"name":  "/dev/sda", "size": "931.5 GiB", "bytes": 1000204886016, "sectors": 1953525168}])
            mock.assert_called_once_with(['/opt/bin/fdisk', '-l', '--bytes', '-x', '-y',  'sda', 'sdb'], env={'LC_NUMERIC': 'C'})

    def test__parse__with_fixtures(self):
        self.maxDiff = None
        for left, right in self.fixture_plan:
            content = fdisk_.FdiskProbe.parse(self.fixtures[left])
            expct = self.fixtures[right]
            self.assertEqual(content, expct)

if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
