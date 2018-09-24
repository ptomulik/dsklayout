#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
from unittest.mock import patch
import os
import os.path
import json

from . import testcase_

import dsklayout.probe.mdadm_ as mdadm_
import dsklayout.probe.backtick_ as backtick_
import dsklayout.probe.composite_ as composite_

backtick = 'dsklayout.util.backtick'

class Test__Convert(unittest.TestCase):

    def test__events__1(self):
        self.assertEqual(mdadm_._Convert.events('123'), 123)

    def test__events__2(self):
        self.assertEqual(mdadm_._Convert.events('-123'), -123)

    def test__events__3(self):
        self.assertEqual(mdadm_._Convert.events('2.34'), (2<<32)|34)

    def test__ord__1(self):
        self.assertEqual(mdadm_._Convert.ord('123'), 123)

    def test__ord__2(self):
        self.assertEqual(mdadm_._Convert.ord('this'), 'this')

    def test__ord__1(self):
        with self.assertRaises(ValueError):
            mdadm_._Convert.ord('foo')

    def test__hex__1(self):
        self.assertEqual(mdadm_._Convert.hex('0x1f'), 0x1f)

    def test__hex__2(self):
        self.assertEqual(mdadm_._Convert.hex('-0x1f'), -0x1f)

    def test__hex__3(self):
        self.assertEqual(mdadm_._Convert.hex('-1f'), -0x1f)

class Test__MdadmBacktickProbe(testcase_.ProbeTestCase):

    @property
    def fixture_plan(self):
        return [
            ('mdadm_detail_1_md1.txt',                  'mdadm_detail_1_md1.content.json'),
            ('mdadm_detail_1_md1_md6.txt',              'mdadm_detail_1_md1_md6.content.json'),
            ('mdadm_examine_1_sda1.txt',                'mdadm_examine_1_sda1.content.json'),
            ('mdadm_examine_1_sda1_sdb1_sda6_sdb6.txt', 'mdadm_examine_1_sda1_sdb1_sda6_sdb6.content.json')
        ]

    def decode_right_fixture(self, content):
        return json.loads(content)

    def test__subclass_of_BackTickProbe(self):
        self.assertTrue(issubclass(mdadm_._MdadmBacktickProbe, backtick_.BackTickProbe))

    def test__command__1(self):
        self.assertEqual(mdadm_._MdadmBacktickProbe.command(), 'mdadm')

    def test__command__2(self):
        self.assertEqual(mdadm_._MdadmBacktickProbe.command(mdadm='foo'), 'foo')

    def test__content(self):
        mdadm = mdadm_._MdadmBacktickProbe('content')
        self.assertIs(mdadm.content, 'content')

    def test__run__with_no_args(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(mdadm_._MdadmBacktickProbe.run(env=dict()), 'ok')
            mock.assert_called_once_with(['mdadm'], env=dict())

    def test__run__with_device(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(mdadm_._MdadmBacktickProbe.run('sda', env=dict()), 'ok')
            mock.assert_called_once_with(['mdadm', 'sda'], env=dict())

    def test__run__with_devices(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(mdadm_._MdadmBacktickProbe.run(['sda', 'sdb'], env=dict()), 'ok')
            mock.assert_called_once_with(['mdadm', 'sda', 'sdb'], env=dict())

    def test__run__with_devices_and_flags(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(mdadm_._MdadmBacktickProbe.run(['sda', 'sdb'], ['-x', '-y'], env=dict()), 'ok')
            mock.assert_called_once_with(['mdadm',  'sda', 'sdb'], env=dict())

    def test__run__with_custom_mdadm(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(mdadm_._MdadmBacktickProbe.run(['sda', 'sdb'], ['-x', '-y'], mdadm='/opt/bin/mdadm', env=dict()), 'ok')
            mock.assert_called_once_with(['/opt/bin/mdadm', 'sda', 'sdb'], env=dict())

    def test__parse__with_fixtures(self):
        self.maxDiff = None
        for left, right in self.fixture_plan:
            content = mdadm_._MdadmBacktickProbe.parse(self.fixtures[left])
            expected = self.fixtures[right]
            self.assertEqual(content, expected)


class Test__MdadmDetailProbe(unittest.TestCase):

    def test__subclass_of_MdadmBacktickProbe(self):
        self.assertTrue(issubclass(mdadm_.MdadmDetailProbe, mdadm_._MdadmBacktickProbe))

    def test__flags__1(self):
        self.assertEqual(mdadm_.MdadmDetailProbe.flags([]), ['--detail'])

    def test__flags__2(self):
        self.assertEqual(mdadm_.MdadmDetailProbe.flags(['-x', '-y']), ['--detail', '-x', '-y'])


class Test__MdadmExamineProbe(unittest.TestCase):

    def test__subclass_of_MdadmBacktickProbe(self):
        self.assertTrue(issubclass(mdadm_.MdadmExamineProbe, mdadm_._MdadmBacktickProbe))

    def test__flags__1(self):
        self.assertEqual(mdadm_.MdadmDetailProbe.flags([]), ['--detail'])

    def test__flags__2(self):
        self.assertEqual(mdadm_.MdadmDetailProbe.flags(['-x', '-y']), ['--detail', '-x', '-y'])


class Test__MdadmProbe(unittest.TestCase):

    def test__subclass_of_CompositeProbe(self):
        self.assertTrue(issubclass(mdadm_.MdadmProbe, composite_.CompositeProbe))


if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
