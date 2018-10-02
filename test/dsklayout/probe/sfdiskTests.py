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
