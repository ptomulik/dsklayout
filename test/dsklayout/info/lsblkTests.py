#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
from unittest.mock import patch
import os.path
import json

import dsklayout.info.lsblk_ as lsblk_
from dsklayout.graph import *

backtick = 'dsklayout.util.backtick'

class Test__LsBlk(unittest.TestCase):

    fixture_plan = [
        ('lsblk_1_all.json',        'lsblk_1_all.graph.json'),
        ('lsblk_1_sda_sdb.json',    'lsblk_1_sda_sdb.graph.json'),
        ('lsblk_1_sda.json',        'lsblk_1_sda.graph.json'),
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
                self._fixtures[left] = json.loads(f.read())
            with open(self.fixture_path(right)) as f:
                self._fixtures[right] = json.loads(f.read())

    def fixture_path(self, file):
        mydir = os.path.dirname(__file__)
        return os.path.join(mydir, 'fixtures', file)

    def test__content(self):
        content = 'content'
        lsblk = lsblk_.LsBlk(content)
        self.assertIs(lsblk.content, content)

    def test__run__with_no_args(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(lsblk_.LsBlk.run(), 'ok')
            mock.assert_called_once_with(['lsblk', '-J', '-O', '-p'])

    def test__run__with_device(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(lsblk_.LsBlk.run('sda'), 'ok')
            mock.assert_called_once_with(['lsblk', '-J', '-O', '-p', 'sda'])

    def test__run__with_devices(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(lsblk_.LsBlk.run(['sda', 'sdb']), 'ok')
            mock.assert_called_once_with(['lsblk', '-J', '-O', '-p', 'sda', 'sdb'])

    def test__run__with_devices_and_flags(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(lsblk_.LsBlk.run(['sda', 'sdb'], ['-x', '-y']), 'ok')
            mock.assert_called_once_with(['lsblk', '-J', '-O', '-p', '-x', '-y',  'sda', 'sdb'])

    def test__run__with_custom_lsblk(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(lsblk_.LsBlk.run(['sda', 'sdb'], ['-x', '-y'], lsblk='/opt/bin/lsblk'), 'ok')
            mock.assert_called_once_with(['/opt/bin/lsblk', '-J', '-O', '-p', '-x', '-y',  'sda', 'sdb'])

    def test__new__with_no_args(self):
        with patch(backtick, return_value='{"foo":"bar"}') as mock:
            lsblk = lsblk_.LsBlk.new()
            self.assertIsInstance(lsblk, lsblk_.LsBlk)
            self.assertEqual(lsblk.content, {"foo":  "bar"})
            mock.assert_called_once_with(['lsblk', '-J', '-O', '-p'])

    def test__new__with_device(self):
        with patch(backtick, return_value='{"foo":"bar"}') as mock:
            lsblk = lsblk_.LsBlk.new('sda')
            self.assertIsInstance(lsblk, lsblk_.LsBlk)
            self.assertEqual(lsblk.content, {"foo":  "bar"})
            mock.assert_called_once_with(['lsblk', '-J', '-O', '-p', 'sda'])

    def test__new__with_devices(self):
        with patch(backtick, return_value='{"foo":"bar"}') as mock:
            lsblk = lsblk_.LsBlk.new(['sda', 'sdb'])
            self.assertIsInstance(lsblk, lsblk_.LsBlk)
            self.assertEqual(lsblk.content, {"foo":  "bar"})
            mock.assert_called_once_with(['lsblk', '-J', '-O', '-p', 'sda', 'sdb'])

    def test__new__with_devices_and_flags(self):
        with patch(backtick, return_value='{"foo":"bar"}') as mock:
            lsblk = lsblk_.LsBlk.new(['sda', 'sdb'], ['-x', '-y'])
            self.assertIsInstance(lsblk, lsblk_.LsBlk)
            self.assertEqual(lsblk.content, {"foo":  "bar"})
            mock.assert_called_once_with(['lsblk', '-J', '-O', '-p', '-x', '-y',  'sda', 'sdb'])

    def test__new__with_custom_lsblk(self):
        with patch(backtick, return_value='{"foo":"bar"}') as mock:
            lsblk = lsblk_.LsBlk.new(['sda', 'sdb'], ['-x', '-y'], lsblk='/opt/bin/lsblk')
            self.assertIsInstance(lsblk, lsblk_.LsBlk)
            self.assertEqual(lsblk.content, {"foo":  "bar"})
            mock.assert_called_once_with(['/opt/bin/lsblk', '-J', '-O', '-p', '-x', '-y',  'sda', 'sdb'])

    def test__graph__with_fixtures(self):
        self.maxDiff = None
        for left, right in self.fixture_plan:
            graph = lsblk_.LsBlk(self.fixtures[left]).graph()
            expct = self.fixtures[right]

            expct["edges"] = [tuple(e) for e in expct["edges"]] # convert json list to tuple

            self.assertEqual(set(graph.edges), set(expct["edges"]))
            self.assertEqual(len(graph.nodes), len(expct["nodes"]))
            for node, props in expct["nodes"].items():
                self.assertEqual(props, graph.nodes[node].properties)

if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
