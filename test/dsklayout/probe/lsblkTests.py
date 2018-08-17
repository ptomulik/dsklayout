#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
from unittest.mock import patch
import os.path
import json

import dsklayout.probe.lsblk_ as lsblk_
from dsklayout.graph import *

backtick = 'dsklayout.util.backtick'

class Test__Properties(unittest.TestCase):

    def test__collective(self):
        self.assertEqual(lsblk_._Properties._collective, ('pkname',))

    def test__properties__1(self):
        # not officially supported, but may be stored
        pro = lsblk_._Properties({'foo':  'FOO', 'bar':  'BAR'})
        self.assertEqual(pro.properties, {'foo':  'FOO', 'bar':  'BAR'})

    def test__properties__2(self):
        # officially supported
        pro = lsblk_._Properties({'name': '/pro/md2', 'fstype':  'ext4'})
        self.assertEqual(pro.properties, {'name': '/pro/md2', 'fstype':  'ext4'})

    def test__properties__3(self):
        # officially supported
        pro = lsblk_._Properties({'name': '/pro/md2', 'pkname':  None})
        self.assertEqual(pro.properties, {'name': '/pro/md2', 'pkname':  None})

    def test__properties__4(self):
        # officially supported
        pro = lsblk_._Properties({'name': '/pro/md2', 'pkname':  '/pro/sda2'})
        self.assertEqual(pro.properties, {'name': '/pro/md2', 'pkname':  '/pro/sda2'})

    def test__set__1(self):
        props = {'name': '/pro/md2', 'fstype':  'ext4'}
        pro = lsblk_._Properties()
        pro.set(props)
        self.assertEqual(pro.properties, props)
        self.assertIsNot(pro.properties, props) # should keep its own copy

    def test__set__2(self):
        pro = lsblk_._Properties({'name': '/pro/md2', 'fstype':  'ext4'})
        pro.set({'fstype':  'xfs', 'mountpoint':  '/home'})
        self.assertEqual(pro.properties, {'fstype': 'xfs', 'mountpoint': '/home'})

    def test__set__3(self):
        pro = lsblk_._Properties({'name': '/pro/md2', 'fstype':  'ext4'})
        pro.set({'fstype':  'xfs', 'pkname':  None})
        self.assertEqual(pro.properties, {'fstype': 'xfs', 'pkname': []})

    def test__set__4(self):
        pro = lsblk_._Properties({'name': '/pro/md2', 'fstype':  'ext4'})
        pro.set({'fstype':  'xfs', 'pkname':  '/pro/sda2'})
        self.assertEqual(pro.properties, {'fstype': 'xfs', 'pkname': ['/pro/sda2']})

    def test__update__0(self):
        props = {'name': '/pro/md2'}
        pro = lsblk_._Properties()
        with self.assertRaises(lsblk_.PropertyError) as context:
            pro.update(props)
        self.assertEqual("Conflicting values for property name: %s vs %s" % (repr(None),repr('/pro/md2')), str(context.exception))

    def test__update__1(self):
        props = {'name': '/pro/md2', 'fstype':  'ext4', 'parttype': '0xfd'}
        pro = lsblk_._Properties(props)
        pro.update(dict(props))
        self.assertIs(pro.properties, props)  # should keep first reference

    def test__update__1__convert(self):
        props = {'name': '/pro/md2', 'fstype':  'ext4', 'parttype': '0xfd'}
        pro = lsblk_._Properties(convert=True).set(props)
        pro.update(props)
        self.assertEqual(pro.properties, {'name': '/pro/md2', 'fstype': 'ext4', 'parttype': 0xfd})

    def test__update__2(self):
        pro = lsblk_._Properties({'name': '/pro/md2', 'fstype':  'ext4', 'mountpoint': '/home'})
        with self.assertRaises(lsblk_.PropertyError) as context:
            pro.update({'name': '/pro/md2', 'fstype':  'xfs'})
        self.assertEqual("Conflicting values for property fstype: %s vs %s" % (repr('ext4'),repr('xfs')), str(context.exception))

    def test__update__3(self):
        pro = lsblk_._Properties({'name': '/pro/md2', 'fstype':  'ext4'})
        pro.update({'pkname': None})
        self.assertEqual(pro.properties, {'name': '/pro/md2', 'fstype': 'ext4', 'pkname': []})

    def test__update__4(self):
        pro = lsblk_._Properties({'name': '/pro/md2', 'fstype':  'ext4'})
        pro.update({'pkname': '/pro/sda2'})
        self.assertEqual(pro.properties, {'name': '/pro/md2', 'fstype': 'ext4', 'pkname': ['/pro/sda2']})
        pro.update({'pkname': '/pro/sdb2'})
        self.assertEqual(pro.properties, {'name': '/pro/md2', 'fstype': 'ext4', 'pkname': ['/pro/sda2', '/pro/sdb2']})
        pro.update({'pkname': '/pro/sda2'}) # no effect, '/pro/sda2' already in pkname
        self.assertEqual(pro.properties, {'name': '/pro/md2', 'fstype': 'ext4', 'pkname': ['/pro/sda2', '/pro/sdb2']})

    def test__new__0(self):
        pro = lsblk_._Properties.new()
        self.assertEqual(pro.properties, dict())

    def test__new__1(self):
        pro = lsblk_._Properties.new({'kname': '/dev/md2', 'pkname': '/dev/sda2', 'ra': '123'})
        self.assertEqual(pro.properties, {'kname': '/dev/md2', 'pkname': ['/dev/sda2'], 'ra': '123'})

    def test__new__2(self):
        pro = lsblk_._Properties.new({'kname': '/dev/md2', 'pkname': '/dev/sda2', 'ra': '123'}, convert=True)
        self.assertEqual(pro.properties, {'kname': '/dev/md2', 'pkname': ['/dev/sda2'], 'ra': 123})

    def test__parttype(self):
        pro = lsblk_._Properties.new({'parttype': '0xfd'})
        self.assertEqual(pro.properties['parttype'], '0xfd')

    def test__parttype__convert(self):
        pro = lsblk_._Properties.new({'parttype': '0xfd'}, convert=True)
        self.assertIs(pro.properties['parttype'], 0xfd)

    def test__parttype__convert_none(self):
        pro = lsblk_._Properties.new({'parttype': None}, convert=True)
        self.assertIs(pro.properties['parttype'], None)

    def test__ra(self):
        pro = lsblk_._Properties.new({'ra': '128'})
        self.assertEqual(pro.properties['ra'], '128')

    def test__ra__convert(self):
        pro = lsblk_._Properties.new({'ra': '128'}, convert=True)
        self.assertIs(pro.properties['ra'], 128)

    def test__ro(self):
        pro = lsblk_._Properties.new({'ro': '0'})
        self.assertEqual(pro.properties['ro'], '0')

    def test__ro__convert_false(self):
        pro = lsblk_._Properties.new({'ro': '0'}, convert=True)
        self.assertIs(pro.properties['ro'], False)

    def test__ro__convert_true(self):
        pro = lsblk_._Properties.new({'ro': '1'}, convert=True)
        self.assertIs(pro.properties['ro'], True)

    def test__rm(self):
        pro = lsblk_._Properties.new({'rm': '0'})
        self.assertEqual(pro.properties['rm'], '0')

    def test__rm__convert_false(self):
        pro = lsblk_._Properties.new({'rm': '0'}, convert=True)
        self.assertIs(pro.properties['rm'], False)

    def test__rm__convert_true(self):
        pro = lsblk_._Properties.new({'rm': '1'}, convert=True)
        self.assertIs(pro.properties['rm'], True)

    def test__hotplug(self):
        pro = lsblk_._Properties.new({'hotplug': '0'})
        self.assertEqual(pro.properties['hotplug'], '0')

    def test__hotplug__convert_false(self):
        pro = lsblk_._Properties.new({'hotplug': '0'}, convert=True)
        self.assertIs(pro.properties['hotplug'], False)

    def test__hotplug__convert_true(self):
        pro = lsblk_._Properties.new({'hotplug': '1'}, convert=True)
        self.assertIs(pro.properties['hotplug'], True)

    def test__alignment(self):
        pro = lsblk_._Properties.new({'alignment': '0'})
        self.assertEqual(pro.properties['alignment'], '0')

    def test__alignment__convert(self):
        pro = lsblk_._Properties.new({'alignment': '0'}, convert=True)
        self.assertIs(pro.properties['alignment'], 0)

    def test__min_io(self):
        pro = lsblk_._Properties.new({'min-io': '512'})
        self.assertEqual(pro.properties['min-io'], '512')

    def test__min_io__convert(self):
        pro = lsblk_._Properties.new({'min-io': '512'}, convert=True)
        self.assertEqual(pro.properties['min-io'], 512)

    def test__opt_io(self):
        pro = lsblk_._Properties.new({'opt-io': '0'})
        self.assertEqual(pro.properties['opt-io'], '0')

    def test__opt_io__convert(self):
        pro = lsblk_._Properties.new({'opt-io': '0'}, convert=True)
        self.assertIs(pro.properties['opt-io'], 0)

    def test__phy_sec(self):
        pro = lsblk_._Properties.new({'phy-sec': '512'})
        self.assertEqual(pro.properties['phy-sec'], '512')

    def test__phy_sec__convert(self):
        pro = lsblk_._Properties.new({'phy-sec': '512'}, convert=True)
        self.assertEqual(pro.properties['phy-sec'], 512)

    def test__log_sec(self):
        pro = lsblk_._Properties.new({'log-sec': '512'})
        self.assertEqual(pro.properties['log-sec'], '512')

    def test__log_sec__convert(self):
        pro = lsblk_._Properties.new({'log-sec': '512'}, convert=True)
        self.assertEqual(pro.properties['log-sec'], 512)

    def test__rota(self):
        pro = lsblk_._Properties.new({'rota': '1'})
        self.assertEqual(pro.properties['rota'], '1')

    def test__rota__convert_false(self):
        pro = lsblk_._Properties.new({'rota': '0'}, convert=True)
        self.assertIs(pro.properties['rota'], False)

    def test__rota__convert_true(self):
        pro = lsblk_._Properties.new({'rota': '1'}, convert=True)
        self.assertIs(pro.properties['rota'], True)

    def test__rq_size(self):
        pro = lsblk_._Properties.new({'rq-size': '128'})
        self.assertEqual(pro.properties['rq-size'], '128')

    def test__rq_size_convert(self):
        pro = lsblk_._Properties.new({'rq-size': '128'}, convert=True)
        self.assertIs(pro.properties['rq-size'], 128)

    def test__rand(self):
        pro = lsblk_._Properties.new({'rand': '1'})
        self.assertEqual(pro.properties['rand'], '1')

    def test__rand__convert_true(self):
        pro = lsblk_._Properties.new({'rand': '1'}, convert=True)
        self.assertIs(pro.properties['rand'], True)

    def test__rand__convert_false(self):
        pro = lsblk_._Properties.new({'rand': '0'}, convert=True)
        self.assertIs(pro.properties['rand'], False)


class Test__LsBlkProbe(unittest.TestCase):

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
        lsblk = lsblk_.LsBlkProbe(content)
        self.assertIs(lsblk.content, content)

    def test__run__with_no_args(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(lsblk_.LsBlkProbe.run(), 'ok')
            mock.assert_called_once_with(['lsblk', '-J', '-O', '-p'])

    def test__run__with_device(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(lsblk_.LsBlkProbe.run('sda'), 'ok')
            mock.assert_called_once_with(['lsblk', '-J', '-O', '-p', 'sda'])

    def test__run__with_devices(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(lsblk_.LsBlkProbe.run(['sda', 'sdb']), 'ok')
            mock.assert_called_once_with(['lsblk', '-J', '-O', '-p', 'sda', 'sdb'])

    def test__run__with_devices_and_flags(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(lsblk_.LsBlkProbe.run(['sda', 'sdb'], ['-x', '-y']), 'ok')
            mock.assert_called_once_with(['lsblk', '-J', '-O', '-p', '-x', '-y',  'sda', 'sdb'])

    def test__run__with_custom_lsblk(self):
        with patch(backtick, return_value='ok') as mock:
            self.assertIs(lsblk_.LsBlkProbe.run(['sda', 'sdb'], ['-x', '-y'], lsblk='/opt/bin/lsblk'), 'ok')
            mock.assert_called_once_with(['/opt/bin/lsblk', '-J', '-O', '-p', '-x', '-y',  'sda', 'sdb'])

    def test__new__with_no_args(self):
        with patch(backtick, return_value='{"foo":"bar"}') as mock:
            lsblk = lsblk_.LsBlkProbe.new()
            self.assertIsInstance(lsblk, lsblk_.LsBlkProbe)
            self.assertEqual(lsblk.content, {"foo":  "bar"})
            mock.assert_called_once_with(['lsblk', '-J', '-O', '-p'])

    def test__new__with_device(self):
        with patch(backtick, return_value='{"foo":"bar"}') as mock:
            lsblk = lsblk_.LsBlkProbe.new('sda')
            self.assertIsInstance(lsblk, lsblk_.LsBlkProbe)
            self.assertEqual(lsblk.content, {"foo":  "bar"})
            mock.assert_called_once_with(['lsblk', '-J', '-O', '-p', 'sda'])

    def test__new__with_devices(self):
        with patch(backtick, return_value='{"foo":"bar"}') as mock:
            lsblk = lsblk_.LsBlkProbe.new(['sda', 'sdb'])
            self.assertIsInstance(lsblk, lsblk_.LsBlkProbe)
            self.assertEqual(lsblk.content, {"foo":  "bar"})
            mock.assert_called_once_with(['lsblk', '-J', '-O', '-p', 'sda', 'sdb'])

    def test__new__with_devices_and_flags(self):
        with patch(backtick, return_value='{"foo":"bar"}') as mock:
            lsblk = lsblk_.LsBlkProbe.new(['sda', 'sdb'], ['-x', '-y'])
            self.assertIsInstance(lsblk, lsblk_.LsBlkProbe)
            self.assertEqual(lsblk.content, {"foo":  "bar"})
            mock.assert_called_once_with(['lsblk', '-J', '-O', '-p', '-x', '-y',  'sda', 'sdb'])

    def test__new__with_custom_lsblk(self):
        with patch(backtick, return_value='{"foo":"bar"}') as mock:
            lsblk = lsblk_.LsBlkProbe.new(['sda', 'sdb'], ['-x', '-y'], lsblk='/opt/bin/lsblk')
            self.assertIsInstance(lsblk, lsblk_.LsBlkProbe)
            self.assertEqual(lsblk.content, {"foo":  "bar"})
            mock.assert_called_once_with(['/opt/bin/lsblk', '-J', '-O', '-p', '-x', '-y',  'sda', 'sdb'])

    def test__graph__with_fixtures(self):
        self.maxDiff = None
        for left, right in self.fixture_plan:
            graph = lsblk_.LsBlkProbe(self.fixtures[left]).graph()
            expct = self.fixtures[right]

            expct["edges"] = [tuple(e) for e in expct["edges"]] # convert json list to tuple

            self.assertEqual(set(graph.edges), set(expct["edges"]))
            self.assertEqual(len(graph.nodes), len(expct["nodes"]))
            for node, props in expct["nodes"].items():
                self.assertEqual(props, graph.nodes[node].properties)

if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
