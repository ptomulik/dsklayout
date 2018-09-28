#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import unittest.mock as mock
from unittest.mock import patch
import json

from . import testcase_

import dsklayout.probe.lvm_ as lvm_
import dsklayout.probe.backtick_ as backtick_
import dsklayout.probe.composite_ as composite_
import dsklayout.probe.lsblk_ as lsblk_

backtick = 'dsklayout.util.backtick'

class LvmXxx(lvm_._LvmBacktickProbe):
    @classmethod
    def cmdname(cls):
        return 'xxx'

class Test__LvmBacktickProbe(testcase_.ProbeTestCase):

    @property
    def fixture_plan(self):
        return [
            ('lvs_1.json',              'lvs_1.content.json'),
            ('lvs_1_teavg-rootfs.json', 'lvs_1_teavg-rootfs.content.json'),
            ('pvs_1.json',              'pvs_1.content.json'),
        ]

    def decode_right_fixture(self, content):
        return json.loads(content)

    def test__subclass_of_BackTickProbe(self):
        self.assertTrue(issubclass(lvm_._LvmBacktickProbe, backtick_.BackTickProbe))

    def test__abstract(self):
        with self.assertRaises(TypeError) as context:
            lvm_._LvmBacktickProbe({})
        self.assertIn('abstract', str(context.exception))

    def test__cmdname(self):
        self.assertIsNone(lvm_._LvmBacktickProbe.cmdname())

    def test__command__1(self):
        with patch('dsklayout.probe.lvm_._LvmBacktickProbe.cmdname', return_value='foo') as cmdname:
            self.assertEqual(lvm_._LvmBacktickProbe.command(), 'foo')
            cmdname.assert_called_once_with()

    def test__command__2(self):
        with patch('dsklayout.probe.lvm_._LvmBacktickProbe.cmdname', return_value='foo') as cmdname:
            self.assertEqual(lvm_._LvmBacktickProbe.command(foo='bar'), 'bar')
            cmdname.assert_called_once_with()

    def test__xflags(self):
        self.assertEqual([], lvm_._LvmBacktickProbe.xflags())

    def test__flags_1(self):
        self.assertEqual(['--readonly', '--reportformat', 'json'], lvm_._LvmBacktickProbe.flags([]))

    def test__flags_2(self):
        self.assertEqual(['--readonly', '--reportformat', 'json', '-x', '-y'], lvm_._LvmBacktickProbe.flags(['-x', '-y']))

    def test__flags_3(self):
        with patch('dsklayout.probe.lvm_._LvmBacktickProbe.xflags', return_value=['--foo']) as xflags:
            self.assertEqual(['--readonly', '--reportformat', 'json', '--foo', '-x', '-y'], lvm_._LvmBacktickProbe.flags(['-x', '-y']))
            xflags.assert_called_once_with()

    def test__parse(self):
        with patch('json.loads', return_value='ok') as loads:
            self.assertIs(lvm_._LvmBacktickProbe.parse("foo"), 'ok')
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
            content = lvm_._LvmBacktickProbe.parse(self.fixtures[left])
            expected = self.fixtures[right]
            self.assertEqual(content, expected)


class Test__LvsProbe(unittest.TestCase):

    def test__subclass_of_LvmBacktickProbe(self):
        self.assertTrue(issubclass(lvm_.LvsProbe, lvm_._LvmBacktickProbe))

    def test__cmdname(self):
        self.assertEqual(lvm_.LvsProbe.cmdname(), 'lvs')

    def test__xflags(self):
        self.assertEqual(lvm_.LvsProbe.xflags(), ['-o', '+lv_all'])


class Test__PvsProbe(unittest.TestCase):

    def test__subclass_of_LvmBacktickProbe(self):
        self.assertTrue(issubclass(lvm_.PvsProbe, lvm_._LvmBacktickProbe))

    def test__cmdname(self):
        self.assertEqual(lvm_.PvsProbe.cmdname(), 'pvs')

    def test__xflags(self):
        self.assertEqual(lvm_.PvsProbe.xflags(), ['-o', '+pv_all'])


class Test__VgsProbe(unittest.TestCase):

    def test__subclass_of_LvmBacktickProbe(self):
        self.assertTrue(issubclass(lvm_.VgsProbe, lvm_._LvmBacktickProbe))

    def test__cmdname(self):
        self.assertEqual(lvm_.VgsProbe.cmdname(), 'vgs')

    def test__xflags(self):
        self.assertEqual(lvm_.VgsProbe.xflags(), ['-o', '+vg_all'])


class Test__LvmProbe(unittest.TestCase):

    def test__subclass_of_CompositeProbe(self):
        self.assertTrue(issubclass(lvm_.LvmProbe, composite_.CompositeProbe))

    def test__new(self):
        graph = mock.Mock()
        graph.nodes = {
                'vol1': mock.Mock(type='lvm'),
                'vol2': mock.Mock(type='lvm'),
                'mem1': mock.Mock(fstype='LVM_member'),
                'mem2': mock.Mock(fstype='LVM_member')
        }
        graph.nodes['vol1'].name = 'vol1'
        graph.nodes['vol2'].name = 'vol2'
        graph.nodes['mem1'].name = 'mem1'
        graph.nodes['mem2'].name = 'mem2'
        pvs = mock.Mock()
        lvs = mock.Mock(content={'report': [{'lv': [{'lv_name': 'vol1', 'vg_name': 'vg1'}, {'lv_name': 'vol2', 'vg_name': 'vg2'}]}]})
        vgs = mock.Mock()
        with patch('dsklayout.probe.composite_.CompositeProbe.extract_lsblk_graph', return_value=graph) as extract_lsblk_graph, \
             patch('dsklayout.probe.lvm_.PvsProbe.new', return_value=pvs) as pvs_new, \
             patch('dsklayout.probe.lvm_.LvsProbe.new', return_value=lvs) as lvs_new, \
             patch('dsklayout.probe.lvm_.VgsProbe.new', return_value=vgs) as vgs_new:
            probe = lvm_.LvmProbe.new()
            self.assertIsInstance(probe, lvm_.LvmProbe)
            extract_lsblk_graph.assert_called_once_with(None, None, dict())
            pvs_new.assert_called_once_with(['mem1', 'mem2'], None)
            lvs_new.assert_called_once_with(['vol1', 'vol2'], None)
            vgs_new.assert_called_once_with(list(set(['vg1', 'vg2'])), None)
            self.assertIs(probe.content['pvs'], pvs)
            self.assertIs(probe.content['lvs'], lvs)
            self.assertIs(probe.content['vgs'], vgs)


    def test__uses__1(self):
        self.assertEqual(lvm_.LvmProbe.uses(), [lvm_.LvsProbe, lvm_.PvsProbe, lvm_.VgsProbe, lsblk_.LsBlkProbe])

    def test__uses__2(self):
        self.assertEqual(lvm_.LvmProbe.uses(lsblkgraph='G'), [lvm_.LvsProbe, lvm_.PvsProbe, lvm_.VgsProbe])

    def test__is_member__1(self):
        item = ('foo', mock.Mock())
        item[1].fstype = 'FOO'
        self.assertFalse(lvm_.LvmProbe._is_member(item))

    def test__is_member__2(self):
        item = ('foo', mock.Mock())
        item[1].fstype = 'LVM_member'
        self.assertTrue(lvm_.LvmProbe._is_member(item))

    def test__is_volume__1(self):
        item = ('foo', mock.Mock())
        item[1].type = 'FOO'
        self.assertFalse(lvm_.LvmProbe._is_volume(item))

    def test__is_volume__2(self):
        item = ('foo', mock.Mock())
        item[1].type = 'lvm'
        self.assertTrue(lvm_.LvmProbe._is_volume(item))


if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
