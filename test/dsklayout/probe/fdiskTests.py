#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
from unittest.mock import patch

from . import testcase_

import os
import os.path
import json

import dsklayout.probe.fdisk_ as fdisk_

backtick = 'dsklayout.util.backtick'

class Test__FdiskProbe(testcase_.ProbeTestCase):

    @property
    def fixture_plan(self):
        return [
            ('fdisk_1_sda_sdb.txt',    'fdisk_1_sda_sdb.content.json'),
            ('fdisk_1_sda.txt',        'fdisk_1_sda.content.json'),
            ('fdisk_2_sda_sdb.txt',    'fdisk_2_sda_sdb.content.json'),
        ]

    def decode_right_fixture(self, content):
        return json.loads(content)

    def test__content(self):
        content = 'content'
        fdisk = fdisk_.FdiskProbe(content)
        self.assertIs(fdisk.content, content)

    def test__entries(self):
        content = [{'name': '/dev/sda', 'foo': 'FOO'},
                   {'name': '/dev/sdb', 'bar': 'BAR'},
                   {'geez': 'Geez'}]
        self.assertEqual(fdisk_.FdiskProbe(content).entries, ['/dev/sda', '/dev/sdb', None])

    def test__partabs(self):
        content = [{'name': '/dev/sda', 'partitions': []},
                   {'name': '/dev/sdb', 'bar': 'BAR'},
                   {'name': '/dev/sdc', 'partitions': []}]
        self.assertEqual(fdisk_.FdiskProbe(content).partabs, ['/dev/sda', '/dev/sdc'])

    def test__entry(self):
        content = [{'name': '/dev/sda', 'foo': 'FOO'},
                   {'name': '/dev/sdb', 'bar': 'BAR'}]
        fdisk = fdisk_.FdiskProbe(content)
        self.assertIs(fdisk.entry('/dev/sda'), content[0])
        self.assertIs(fdisk.entry('/dev/sdb'), content[1])
        with self.assertRaises(ValueError) as context:
            fdisk.entry('/dev/sdc')
        self.assertEqual(("invalid device name: %s" % repr('/dev/sdc')), str(context.exception))

    def test__partab(self):
        sda1_i = {'device': '/dev/sda1',
                  'start': 'START A1',
                  'end': 'END A1',
                  'sectors': 'SECTORS A1',
                  'uuid': 'UUID A1',
                  'type-uuid': 'TYPE UUID A1',
                  'name': 'NAME A1',
                  'type': 'TYPE A1'}
        sda1_o = {'device': '/dev/sda1',
                  'start': 'START A1',
                  'end': 'END A1',
                  'size': 'SECTORS A1',
                  'uuid': 'UUID A1',
                  'type': 'TYPE UUID A1',
                  'name': 'NAME A1',
                  'typename': 'TYPE A1'}
        sda2_i = {'device': '/dev/sda2',
                  'start': 'START A2',
                  'end': 'END A2',
                  'sectors': 'SECTORS A2',
                  'uuid': 'UUID A2',
                  'id': 'ID A2',
                  'name': 'NAME A2',
                  'type': 'TYPE A2'}
        sda2_o = {'device': '/dev/sda2',
                  'start': 'START A2',
                  'end': 'END A2',
                  'size': 'SECTORS A2',
                  'uuid': 'UUID A2',
                  'type': 'ID A2',
                  'name': 'NAME A2',
                  'typename': 'TYPE A2'}
        sdb1_i = {'device': '/dev/sdb1',
                  'start': 'START B1',
                  'end': 'END B1',
                  'sectors': 'SECTORS B1',
                  'uuid': 'UUID B1',
                  'type-uuid': 'TYPE UUID B1',
                  'name': 'NAME B1',
                  'type': 'TYPE B1'}
        sdb1_o = {'device': '/dev/sdb1',
                  'start': 'START B1',
                  'end': 'END B1',
                  'size': 'SECTORS B1',
                  'uuid': 'UUID B1',
                  'type': 'TYPE UUID B1',
                  'name': 'NAME B1',
                  'typename': 'TYPE B1'}

        sda_i = {'name': '/dev/sda',
                 'disklabel_type': 'DISKLABEL TYPE A',
                 'disk_identifier': 'DISK IDENTIFIER A',
                 'units': 'UNITS A',
                 'bytes': 'BYTES A',
                 'columns': 'COLUMNS A',
                 'partitions': [sda1_i, sda2_i]}

        sda_o = {'device': '/dev/sda',
                 'label': 'DISKLABEL TYPE A',
                 'id': 'DISK IDENTIFIER A',
                 'units': 'UNITS A',
                 'bytes': 'BYTES A',
                 'partitions': [sda1_o, sda2_o]}

        sdb_i = {'name': '/dev/sdb',
                 'disklabel_type': 'DISKLABEL TYPE B',
                 'disk_identifier': 'DISK IDENTIFIER B',
                 'units': 'UNITS B',
                 'bytes': 'BYTES B',
                 'columns': 'COLUMNS B',
                 'partitions': [sdb1_i]}

        sdb_o = {'device': '/dev/sdb',
                 'label': 'DISKLABEL TYPE B',
                 'id': 'DISK IDENTIFIER B',
                 'units': 'UNITS B',
                 'bytes': 'BYTES B',
                 'partitions': [sdb1_o]}

        sdc_i = {'name': '/dev/sdc',
                 'disklabel_type': 'DISKLABEL TYPE C',
                 'disk_identifier': 'DISK IDENTIFIER C',
                 'units': 'UNITS C',
                 'bytes': 'BYTES C',
                 'columns': 'COLUMNS C'}


        fdisk = fdisk_.FdiskProbe([sda_i, sdb_i, sdc_i])
        self.maxDiff = None
        self.assertEqual(fdisk.partab('/dev/sda'), sda_o)
        self.assertEqual(fdisk.partab('/dev/sdb'), sdb_o)

        with self.assertRaises(ValueError) as context:
            fdisk.partab('/dev/sdc')
        self.assertEqual(("entry %s has no partition table" % repr('/dev/sdc')), str(context.exception))
        with self.assertRaises(ValueError) as context:
            fdisk.partab('/dev/sdd')
        self.assertEqual(("invalid device name: %s" % repr('/dev/sdd')), str(context.exception))

    def test__command_1(self):
        self.assertEqual(fdisk_.FdiskProbe.command(), 'fdisk')

    def test__command_2(self):
        self.assertEqual(fdisk_.FdiskProbe.command(fdisk='/opt/bin/fdisk'), '/opt/bin/fdisk')

    def test__flags__1(self):
        self.assertEqual(fdisk_.FdiskProbe.flags([]), ['-l', '--bytes'])

    def test__flags__2(self):
        self.assertEqual(fdisk_.FdiskProbe.flags(['-x']), ['-l', '--bytes', '-x'])

    def test__kwargs__1(self):
        with patch.dict('os.environ', {'foo': 'FOO'}, True):
            self.assertEqual(fdisk_.FdiskProbe.kwargs(), {'env': {'foo': 'FOO', 'LC_NUMERIC':'C'}})

    def test__kwargs__2(self):
        with patch.dict('os.environ', {'foo': 'FOO'}, True):
            self.assertEqual(fdisk_.FdiskProbe.kwargs(env={'bar': 'BAR'}), {'env': {'bar': 'BAR', 'LC_NUMERIC':'C'}})

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
            expected = self.fixtures[right]
            self.assertEqual(content, expected)

    def test__parse__1(self):
        self.assertEqual(fdisk_.FdiskProbe.parse('bleah'), [{}])

if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
