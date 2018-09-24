#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
from unittest.mock import patch
import os
import os.path
import json

import dsklayout.probe.lvm_ as lvm_
import dsklayout.probe.backtick_ as backtick_
import dsklayout.probe.composite_ as composite_

backtick = 'dsklayout.util.backtick'

class LvmXxx(lvm_._LvmReportProbe):
    @classmethod
    def cmdname(cls):
        return 'xxx'


class Test__LvmReportProbe(unittest.TestCase):

    fixture_plan = [
        ('lvs_1.json',
         'lvs_1.content.json'),
        ('lvs_1_teavg-rootfs.json',
         'lvs_1_teavg-rootfs.content.json'),
        ('pvs_1.json',
         'pvs_1.content.json'),
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

    def test__subclass_of_BackTickProbe(self):
        self.assertTrue(issubclass(lvm_._LvmReportProbe, backtick_.BackTickProbe))

    def test__abstract(self):
        with self.assertRaises(TypeError) as context:
            lvm_._LvmReportProbe({})
        self.assertIn('abstract', str(context.exception))

    def test__cmdname(self):
        self.assertIsNone(lvm_._LvmReportProbe.cmdname())

    def test__command__1(self):
        with patch('dsklayout.probe.lvm_._LvmReportProbe.cmdname', return_value='foo') as cmdname:
            self.assertEqual(lvm_._LvmReportProbe.command(), 'foo')
            cmdname.assert_called_once_with()

    def test__command__2(self):
        with patch('dsklayout.probe.lvm_._LvmReportProbe.cmdname', return_value='foo') as cmdname:
            self.assertEqual(lvm_._LvmReportProbe.command(foo='bar'), 'bar')
            cmdname.assert_called_once_with()

    def test__xflags(self):
        self.assertEqual([], lvm_._LvmReportProbe.xflags())

    def test__flags_1(self):
        self.assertEqual(['--readonly', '--reportformat', 'json'], lvm_._LvmReportProbe.flags([]))

    def test__flags_2(self):
        self.assertEqual(['--readonly', '--reportformat', 'json', '-x', '-y'], lvm_._LvmReportProbe.flags(['-x', '-y']))

    def test__flags_3(self):
        with patch('dsklayout.probe.lvm_._LvmReportProbe.xflags', return_value=['--foo']) as xflags:
            self.assertEqual(['--readonly', '--reportformat', 'json', '--foo', '-x', '-y'], lvm_._LvmReportProbe.flags(['-x', '-y']))
            xflags.assert_called_once_with()

    def test__parse(self):
        with patch('json.loads', return_value='ok') as loads:
            self.assertIs(lvm_._LvmReportProbe.parse("foo"), 'ok')
            loads.assert_called_once_with("foo")

    def test__content(self):
        lvm = LvmXxx('content')
        self.assertIs(lvm.content, 'content')

    def test__run__with_no_args(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(LvmXxx.run(env=dict()), 'ok')
            mock.assert_called_once_with(['xxx', '--readonly', '--reportformat', 'json'], env=dict())

    def test__run__with_device(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(LvmXxx.run('sda', env=dict()), 'ok')
            mock.assert_called_once_with(['xxx', '--readonly', '--reportformat', 'json', 'sda'], env=dict())

    def test__run__with_devices(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(LvmXxx.run(['sda', 'sdb'], env=dict()), 'ok')
            mock.assert_called_once_with(['xxx', '--readonly', '--reportformat', 'json', 'sda', 'sdb'], env=dict())

    def test__run__with_devices_and_flags(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(LvmXxx.run(['sda', 'sdb'], ['-x', '-y'], env=dict()), 'ok')
            mock.assert_called_once_with(['xxx', '--readonly', '--reportformat', 'json',  '-x', '-y', 'sda', 'sdb'], env=dict())

    def test__run__with_custom_xxx(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(LvmXxx.run(['sda', 'sdb'], ['-x', '-y'], xxx='/opt/bin/xxx', env=dict()), 'ok')
            mock.assert_called_once_with(['/opt/bin/xxx', '--readonly', '--reportformat', 'json',  '-x', '-y', 'sda', 'sdb'], env=dict())

    def test__parse__with_fixtures(self):
        self.maxDiff = None
        for left, right in self.fixture_plan:
            content = lvm_._LvmReportProbe.parse(self.fixtures[left])
            expected = self.fixtures[right]
            self.assertEqual(content, expected)


class Test__LvsProbe(unittest.TestCase):

    def test__subclass_of_LvmReportProbe(self):
        self.assertTrue(issubclass(lvm_.LvsProbe, lvm_._LvmReportProbe))

    def test__cmdname(self):
        self.assertEqual(lvm_.LvsProbe.cmdname(), 'lvs')

    def test__xflags(self):
        self.assertEqual(lvm_.LvsProbe.xflags(), ['-o', '+lv_all'])


class Test__PvsProbe(unittest.TestCase):

    def test__subclass_of_LvmReportProbe(self):
        self.assertTrue(issubclass(lvm_.PvsProbe, lvm_._LvmReportProbe))

    def test__cmdname(self):
        self.assertEqual(lvm_.PvsProbe.cmdname(), 'pvs')

    def test__xflags(self):
        self.assertEqual(lvm_.PvsProbe.xflags(), ['-o', '+pv_all'])


class Test__VgsProbe(unittest.TestCase):

    def test__subclass_of_LvmReportProbe(self):
        self.assertTrue(issubclass(lvm_.VgsProbe, lvm_._LvmReportProbe))

    def test__cmdname(self):
        self.assertEqual(lvm_.VgsProbe.cmdname(), 'vgs')

    def test__xflags(self):
        self.assertEqual(lvm_.VgsProbe.xflags(), ['-o', '+vg_all'])


class Test__LvmProbe(unittest.TestCase):

    def test__subclass_of_CompositeProbe(self):
        self.assertTrue(issubclass(lvm_.LvmProbe, composite_.CompositeProbe))


if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
