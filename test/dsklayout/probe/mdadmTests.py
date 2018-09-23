#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
from unittest.mock import patch
import os
import os.path
import json

import dsklayout.probe.mdadm_ as mdadm_
import dsklayout.probe.backtick_ as backtick_
import dsklayout.probe.probe_ as probe_

backtick = 'dsklayout.util.backtick'

class Test__MdadmReportProbe(unittest.TestCase):

    fixture_plan = [
        ('mdadm_detail_1_md1.txt',
         'mdadm_detail_1_md1.content.json'),
        ('mdadm_detail_1_md1_md6.txt',
         'mdadm_detail_1_md1_md6.content.json'),
        ('mdadm_examine_1_sda1.txt',
         'mdadm_examine_1_sda1.content.json'),
        ('mdadm_examine_1_sda1_sdb1_sda6_sdb6.txt',
         'mdadm_examine_1_sda1_sdb1_sda6_sdb6.content.json')
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
        self.assertTrue(issubclass(mdadm_._MdadmReportProbe, backtick_.BackTickProbe))

    def test__command__1(self):
        self.assertEqual(mdadm_._MdadmReportProbe.command(), 'mdadm')

    def test__command__2(self):
        self.assertEqual(mdadm_._MdadmReportProbe.command(mdadm='foo'), 'foo')

    def test__content(self):
        content = 'content'
        mdadm = mdadm_.MdadmProbe(content)
        self.assertIs(mdadm.content, content)

    def test__run__with_no_args(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(mdadm_._MdadmReportProbe.run(env=dict()), 'ok')
            mock.assert_called_once_with(['mdadm'], env=dict())

    def test__run__with_device(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(mdadm_._MdadmReportProbe.run('sda', env=dict()), 'ok')
            mock.assert_called_once_with(['mdadm', 'sda'], env=dict())

    def test__run__with_devices(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(mdadm_._MdadmReportProbe.run(['sda', 'sdb'], env=dict()), 'ok')
            mock.assert_called_once_with(['mdadm', 'sda', 'sdb'], env=dict())

    def test__run__with_devices_and_flags(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(mdadm_._MdadmReportProbe.run(['sda', 'sdb'], ['-x', '-y'], env=dict()), 'ok')
            mock.assert_called_once_with(['mdadm',  'sda', 'sdb'], env=dict())

    def test__run__with_custom_mdadm(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(mdadm_._MdadmReportProbe.run(['sda', 'sdb'], ['-x', '-y'], mdadm='/opt/bin/mdadm', env=dict()), 'ok')
            mock.assert_called_once_with(['/opt/bin/mdadm', 'sda', 'sdb'], env=dict())

    def test__parse__with_fixtures(self):
        self.maxDiff = None
        for left, right in self.fixture_plan:
            content = mdadm_._MdadmReportProbe.parse(self.fixtures[left])
            expected = self.fixtures[right]
            self.assertEqual(content, expected)


class Test__MdadmDetailProbe(unittest.TestCase):

    def test__subclass_of_MdadmReportProbe(self):
        self.assertTrue(issubclass(mdadm_.MdadmDetailProbe, mdadm_._MdadmReportProbe))

    def test__flags__1(self):
        self.assertEqual(mdadm_.MdadmDetailProbe.flags([]), ['--detail'])

    def test__flags__2(self):
        self.assertEqual(mdadm_.MdadmDetailProbe.flags(['-x', '-y']), ['--detail', '-x', '-y'])


class Test__MdadmExamineProbe(unittest.TestCase):

    def test__subclass_of_MdadmReportProbe(self):
        self.assertTrue(issubclass(mdadm_.MdadmExamineProbe, mdadm_._MdadmReportProbe))

    def test__flags__1(self):
        self.assertEqual(mdadm_.MdadmDetailProbe.flags([]), ['--detail'])

    def test__flags__2(self):
        self.assertEqual(mdadm_.MdadmDetailProbe.flags(['-x', '-y']), ['--detail', '-x', '-y'])


class Test__MdadmProbe(unittest.TestCase):

    def test__subclass_of_Probe(self):
        self.assertTrue(issubclass(mdadm_.MdadmProbe, probe_.Probe))

    def test__not_subclass_of_BacktickProbe(self):
        self.assertFalse(issubclass(mdadm_.MdadmProbe, backtick_.BackTickProbe))


if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
