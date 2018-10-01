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


class Test__MdadmParser(testcase_.ProbeTestCase):

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

    def test__convert__raid_devices(self):
        self.assertEqual(mdadm_._MdadmParser.convert('raid_devices', '123'), 123)
        with self.assertRaises(ValueError):
            mdadm_._MdadmParser.convert('raid_devices', 'foo')

    def test__convert__total_devices(self):
        self.assertEqual(mdadm_._MdadmParser.convert('total_devices', '123'), 123)
        with self.assertRaises(ValueError):
            mdadm_._MdadmParser.convert('total_devices', 'foo')

    def test__convert__preferred_minor(self):
        self.assertEqual(mdadm_._MdadmParser.convert('preferred_minor', '123'), 123)
        with self.assertRaises(ValueError):
            mdadm_._MdadmParser.convert('preferred_minor', 'foo')

    def test__convert__active_devices(self):
        self.assertEqual(mdadm_._MdadmParser.convert('active_devices', '123'), 123)
        with self.assertRaises(ValueError):
            mdadm_._MdadmParser.convert('active_devices', 'foo')

    def test__convert__working_devices(self):
        self.assertEqual(mdadm_._MdadmParser.convert('working_devices', '123'), 123)
        with self.assertRaises(ValueError):
            mdadm_._MdadmParser.convert('working_devices', 'foo')

    def test__convert__failed_devices(self):
        self.assertEqual(mdadm_._MdadmParser.convert('failed_devices', '123'), 123)
        with self.assertRaises(ValueError):
            mdadm_._MdadmParser.convert('failed_devices', 'foo')

    def test__convert__spare_devices(self):
        self.assertEqual(mdadm_._MdadmParser.convert('spare_devices', '123'), 123)
        with self.assertRaises(ValueError):
            mdadm_._MdadmParser.convert('spare_devices', 'foo')

    def test__convert__events__1(self):
        self.assertEqual(mdadm_._MdadmParser.convert('events', '123'), 123)
        with self.assertRaises(ValueError):
            mdadm_._MdadmParser.convert('events', 'foo')

    def test__convert__events__2(self):
        self.assertEqual(mdadm_._MdadmParser.convert('events', '12.34'), ((12<<32)|34))

    def test__convert__number(self):
        self.assertEqual(mdadm_._MdadmParser.convert('number', '123'), 123)
        with self.assertRaises(ValueError):
            mdadm_._MdadmParser.convert('number', 'foo')

    def test__convert__major(self):
        self.assertEqual(mdadm_._MdadmParser.convert('major', '123'), 123)
        with self.assertRaises(ValueError):
            mdadm_._MdadmParser.convert('major', 'foo')

    def test__convert__minor(self):
        self.assertEqual(mdadm_._MdadmParser.convert('minor', '123'), 123)
        with self.assertRaises(ValueError):
            mdadm_._MdadmParser.convert('minor', 'foo')

    def test__convert__raid_device(self):
        self.assertEqual(mdadm_._MdadmParser.convert('raid_device', '123'), 123)
        with self.assertRaises(ValueError):
            mdadm_._MdadmParser.convert('raid_device', 'foo')

    def test__convert__feature_map__1(self):
        self.assertEqual(mdadm_._MdadmParser.convert('feature_map', '123'), 0x123)
        with self.assertRaises(ValueError):
            mdadm_._MdadmParser.convert('feature_map', 'foo')

    def test__convert__feature_map__2(self):
        self.assertEqual(mdadm_._MdadmParser.convert('feature_map', '0x123'), 0x123)
        with self.assertRaises(ValueError):
            mdadm_._MdadmParser.convert('feature_map', 'foo')

    def test__match_device_name__1(self):
        m = mdadm_._MdadmParser._match_device_name('//dev:')
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), '//dev')

    def test__match_device_name__2(self):
        m = mdadm_._MdadmParser._match_device_name('/dev:')
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), '/dev')

    def test__match_device_name__3(self):
        m = mdadm_._MdadmParser._match_device_name('  /dev/sda1:  ')
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), '/dev/sda1')

    def test__match_device_name__4(self):
        self.assertIsNone(mdadm_._MdadmParser._match_device_name('foo'))

    def test__parse_device_name__1(self):
        node = dict()
        self.assertTrue(mdadm_._MdadmParser._parse_device_name(node, '  //dev:  '))
        self.assertEqual(node['device_name'], '//dev')

    def test__parse_device_name__2(self):
        node = dict()
        self.assertTrue(mdadm_._MdadmParser._parse_device_name(node, '  /dev/sda1:  '))
        self.assertEqual(node['device_name'], '/dev/sda1')

    def test__parse_device_name__3(self):
        node = dict()
        self.assertFalse(mdadm_._MdadmParser._parse_device_name(node, 'foo'))

    def test__parse_device_name__4(self):
        node = dict()
        self.assertFalse(mdadm_._MdadmParser._parse_device_name(node, '/dev/sda'))

    def test__parse_keyval__0(self):
        node = dict()
        self.assertTrue(mdadm_._MdadmParser._parse_keyval(node, '  foo: bar '))
        self.assertEqual(node['foo'], 'bar')

    def test__parse_keyval__1(self):
        node = dict()
        self.assertTrue(mdadm_._MdadmParser._parse_keyval(node, '  raid_devices: 2 '))
        self.assertEqual(node['raid_devices'], 2)

    def test__parse_keyval__2(self):
        node = dict()
        self.assertFalse(mdadm_._MdadmParser._parse_keyval(node, '  raid_devices: x '))
        self.assertEqual(node, dict())

    def test__parse_keyval__3(self):
        node = dict()
        self.assertTrue(mdadm_._MdadmParser._parse_keyval(node, '  events: 2.34 '))
        self.assertEqual(node['events'], ((2<<32)|34))

    def test__parse_table_header__1(self):
        node = dict()
        self.assertFalse(mdadm_._MdadmParser._parse_table_header(node, 'foo'))
        self.assertEqual(node, dict())

    def test__parse_table_header__2(self):
        node = dict()
        #                                                                          1111111111222222222233333333334
        #                                                                01234567890123456789012345678901234567890
        self.assertTrue(mdadm_._MdadmParser._parse_table_header(node, '  Number  Major  Minor  RaidDevice  State'))
        self.assertEqual(node, {'table': {'headers': ('Number', 'Major', 'Minor', 'RaidDevice', 'State'), 'colspan': [(2,8), (10,15), (17,22), (24,34), (36,41)]}})

    def test__parse_table_row__1(self):
        node = dict()
        self.assertFalse(mdadm_._MdadmParser._parse_table_row(node, '  Foo  Bar Geez  '))
        self.assertEqual(node, dict())

    def test__parse_table_row__2(self):
        node = {'table': {
            'headers': ('Number', 'Major', 'Minor', 'RaidDevice', 'State'),
            'colspan': [(2,8), (10,15), (17,22), (24,34), (36,41)]
        }}
        #                                                                     1111111111222222222233333333334
        #                                                           01234567890123456789012345678901234567890
        #                                                             ------  -----  -----  ----------  -----
        self.assertTrue(mdadm_._MdadmParser._parse_table_row(node, '    0       8     18         0      active sync   /dev/sdb1'))
        self.assertEqual(node['table']['rows'][-1], {'number': 0, 'major': 8, 'minor': 18, 'raid_device': 0, 'state': ['active', 'sync'], 'device': '/dev/sdb1'})
        self.assertTrue(mdadm_._MdadmParser._parse_table_row(node, '    1       8      2         1      active sync   /dev/sda1'))
        self.assertEqual(node['table']['rows'][-1], {'number': 1, 'major': 8, 'minor': 2, 'raid_device': 1, 'state': ['active', 'sync'], 'device': '/dev/sda1'})

    def test__parse__with_fixtures(self):
        self.maxDiff = None
        for left, right in self.fixture_plan:
            content = mdadm_._MdadmBacktickProbe.parse(self.fixtures[left])
            expected = self.fixtures[right]
            self.assertEqual(content, expected)


class Test__MdadmBacktickProbe(unittest.TestCase):

    def test__subclass_of_BackTickProbe(self):
        self.assertTrue(issubclass(mdadm_._MdadmBacktickProbe, backtick_.BackTickProbe))

    def test__cmdname(self):
        self.assertEqual(mdadm_._MdadmBacktickProbe.cmdname(), 'mdadm')

    def test__command(self):
        self.assertIs(mdadm_._MdadmBacktickProbe.command.__code__, backtick_.BackTickProbe.command.__code__)

    def test__flags(self):
        self.assertIs(mdadm_._MdadmBacktickProbe.flags.__code__, backtick_.BackTickProbe.flags.__code__)

    def test__kwargs(self):
        self.assertIs(mdadm_._MdadmBacktickProbe.kwargs.__code__, backtick_.BackTickProbe.kwargs.__code__)

    def test__run(self):
        self.assertIs(mdadm_._MdadmBacktickProbe.run.__code__, backtick_.BackTickProbe.run.__code__)

    def test__new(self):
        self.assertIs(mdadm_._MdadmBacktickProbe.new.__code__, backtick_.BackTickProbe.new.__code__)

    def test__content(self):
        mdadm = mdadm_._MdadmBacktickProbe('content')
        self.assertIs(mdadm.content, 'content')

    def test__parse(self):
        with patch.object(mdadm_._MdadmParser, 'parse', return_value='ok') as parse:
            self.assertIs(mdadm_._MdadmBacktickProbe.parse('foo'), 'ok')
            parse.assert_called_once_with('foo')


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
