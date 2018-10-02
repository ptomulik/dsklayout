#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import unittest.mock as mock
from unittest.mock import patch
import os.path
import json

import dsklayout.probe.sfdisk_ as sfdisk_
import dsklayout.probe.backtick_ as backtick_

import test.dsklayout.probe.testcase_ as testcase_

backtick = 'dsklayout.util.backtick'

class Test__SfdiskProbe(testcase_.ProbeTestCase):

    @property
    def fixture_plan(self):
        return [ ('sfdisk_1_sda.json', 'sfdisk_1_sda.content.json') ]

    def decode_right_fixture(self, content):
        return json.loads(content)

    def test__is_subclass_of_BacktickProbe(self):
        self.assertTrue(issubclass(sfdisk_.SfdiskProbe, backtick_.BackTickProbe))

    def test__content(self):
        content = mock.Mock()
        sfdisk = sfdisk_.SfdiskProbe(content)
        self.assertIs(sfdisk.content, content)

    def test__run(self):
        self.assertIs(sfdisk_.SfdiskProbe.run.__code__, backtick_.BackTickProbe.run.__code__)

    def test__new(self):
        self.assertIs(sfdisk_.SfdiskProbe.new.__code__, backtick_.BackTickProbe.new.__code__)

    def test__command(self):
        self.assertIs(sfdisk_.SfdiskProbe.command.__code__, backtick_.BackTickProbe.command.__code__)

    def test__kwargs(self):
        self.assertIs(sfdisk_.SfdiskProbe.kwargs.__code__, backtick_.BackTickProbe.kwargs.__code__)

    def test__entries__1(self):
        device = mock.Mock(spec=True)
        probe = sfdisk_.SfdiskProbe({'partitiontable': {'device': device}})
        self.assertEqual(probe.entries, [device])
        self.assertIs(probe.entries[0], device)

    def test__entries__2(self):
        probe = sfdisk_.SfdiskProbe({'partitiontable': dict()})
        self.assertEqual(probe.entries, [None])

    def test__entries__3(self):
        probe = sfdisk_.SfdiskProbe(dict())
        with self.assertRaises(KeyError) as context:
            probe.entries
        self.assertIn('partitiontable', str(context.exception))

    def test__partabs__1(self):
        device = mock.Mock(spec=True)
        probe = sfdisk_.SfdiskProbe({'partitiontable': {'device': device}})
        self.assertEqual(probe.partabs, [device])
        self.assertIs(probe.partabs[0], device)

    def test__partabs__2(self):
        probe = sfdisk_.SfdiskProbe({'partitiontable': dict()})
        self.assertEqual(probe.partabs, [None])

    def test__partabs__3(self):
        probe = sfdisk_.SfdiskProbe(dict())
        with self.assertRaises(KeyError) as context:
            probe.partabs
        self.assertIn('partitiontable', str(context.exception))

    def test__entry__1(self):
        entry = {'device': '/dev/sda', 'foo': 'bar'}
        probe = sfdisk_.SfdiskProbe({'partitiontable': entry})
        self.assertIs(probe.entry('/dev/sda'), entry)

    def test__entry__2(self):
        entry = {'device': '/dev/sdb', 'foo': 'bar'}
        probe = sfdisk_.SfdiskProbe({'partitiontable': entry})
        with self.assertRaises(ValueError) as context:
            self.assertIs(probe.entry('/dev/sda'), entry)
        self.assertEqual(str(context.exception), "invalid device name: %s" % repr('/dev/sda'))

    def test__entry__3(self):
        entry = {'foo': 'bar'}
        probe = sfdisk_.SfdiskProbe({'partitiontable': entry})
        with self.assertRaises(ValueError) as context:
            self.assertIs(probe.entry('/dev/sda'), entry)
        self.assertEqual(str(context.exception), "invalid device name: %s" % repr('/dev/sda'))

    def test__partab__1(self):
        entry = {'device': '/dev/sda', 'foo': 'bar'}
        probe = sfdisk_.SfdiskProbe({'partitiontable': entry})
        with self.assertRaises(KeyError) as context:
            probe.partab('/dev/sda')
        self.assertIn('partitions', str(context.exception))

    def test__partab__2(self):
        partitions = []
        entry = {'device': '/dev/sda', 'partitions': partitions}
        probe = sfdisk_.SfdiskProbe({'partitiontable': entry})
        pt = probe.partab('/dev/sda')
        self.assertEqual(pt, entry)
        self.assertIsNot(pt, entry)

    def test__partab__3(self):
        partitions = [{'node': 'NODE A1',
                       'start': 'START A1',
                       'size': 'SIZE A1',
                       'uuid': 'UUID A1',
                       'type': 'TYPE A1',
                       'name': 'NAME A1'}]
        entry = {'device': '/dev/sda',
                 'label': 'LABEL A',
                 'id': 'ID A',
                 'unit': 'UNIT A',
                 'partitions': partitions}
        probe = sfdisk_.SfdiskProbe({'partitiontable': entry})
        pt = probe.partab('/dev/sda')
        self.assertEqual(pt, {'device': '/dev/sda',
                              'label': 'LABEL A',
                              'id': 'ID A',
                              'units': 'UNIT A',
                              'partitions': [
                                  {'device': 'NODE A1',
                                   'start': 'START A1',
                                   'size': 'SIZE A1',
                                   'uuid': 'UUID A1',
                                   'type': 'TYPE A1',
                                   'name': 'NAME A1'}
                                  ]
                              })
        self.assertIsNot(pt, entry)

    def test__cmdname(self):
        self.assertEqual(sfdisk_.SfdiskProbe.cmdname(), 'sfdisk')

    def test__flags__1(self):
        self.assertEqual(sfdisk_.SfdiskProbe.flags([]), ['-J'])

    def test__flags__2(self):
        self.assertEqual(sfdisk_.SfdiskProbe.flags(['-x', '-y']), ['-J', '-x', '-y'])

    def test__parse__1(self):
        self.assertEqual(sfdisk_.SfdiskProbe.parse('{"foo": ["bar1", "bar2"]}'), {"foo": ["bar1", "bar2"]})

    def test__parse__with_fixtures(self):
        self.maxDiff = None
        for left, right in self.fixture_plan:
            content = sfdisk_.SfdiskProbe.parse(self.fixtures[left])
            expected = self.fixtures[right]
            self.assertEqual(content, expected)


if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
