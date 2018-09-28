#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
from unittest.mock import patch

from . import testcase_

import os.path
import json

import dsklayout.probe.fdiskparser_ as fdiskparser_
import dsklayout.probe.backtick_ as backtick_

backtick = 'dsklayout.util.backtick'

class Test__FdiskParser(testcase_.ProbeTestCase):

    @property
    def fixture_plan(self):
        return [
            ('fdisk_1_sda_sdb.txt',    'fdisk_1_sda_sdb.content.json'),
            ('fdisk_1_sda.txt',        'fdisk_1_sda.content.json'),
            ('fdisk_2_sda_sdb.txt',    'fdisk_2_sda_sdb.content.json'),
        ]

    def decode_right_fixture(self, content):
        return json.loads(content)

    def test__parse__with_fixtures(self):
        self.maxDiff = None
        for left, right in self.fixture_plan:
            content = fdiskparser_.FdiskParser().parse(self.fixtures[left])
            expected = self.fixtures[right]
            self.assertEqual(content, expected)

    def test__parse__1(self):
        self.assertEqual(fdiskparser_.FdiskParser().parse('bleah'), [{}])

    def test__parse__2(self):
        text = 'Disk /dev/sda: 931.5 GiB, 1000204886016 bytes, 1953525168 sectors'
        content = [{"name":  "/dev/sda", "size": "931.5 GiB", "bytes": 1000204886016, "sectors": 1953525168}]
        self.assertEqual(fdiskparser_.FdiskParser().parse(text), content)


    def test__adjust_right__1(self):
        #          00000000001111
        #          01234567890123
        #          .  |<
        pattern = "*** **** *****"
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 0, 1, None), 3)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 0, 2, None), 3)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 0, 3, None), 3)

        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 1, 1, None), 3)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 1, 2, None), 3)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 1, 3, None), 3)

        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 2, 1, None), 3)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 2, 2, None), 3)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 2, 3, None), 3)

        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 0, 7, None), 7)

    def test__adjust_right__2(self):
        #          00000000001111
        #          01234567890123
        #              .   |<
        pattern = "*** **** *****"
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 4, 5, None), 8)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 4, 6, None), 8)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 4, 7, None), 8)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 4, 8, None), 8)

        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 5, 5, None), 8)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 5, 6, None), 8)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 5, 7, None), 8)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 5, 8, None), 8)

        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 6, 5, None), 8)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 6, 6, None), 8)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 6, 7, None), 8)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 6, 8, None), 8)

        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 7, 5, None), 8)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 7, 6, None), 8)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 7, 7, None), 8)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 7, 8, None), 8)

    def test__adjust_right__3(self):
        #          00000000001111
        #          01234567890123
        #                   .    |<
        pattern = "*** **** *****"
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 9, 10, None), 14)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 9, 11, None), 14)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 9, 12, None), 14)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 9, 13, None), 14)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 9, 14, None), 14)

        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 10, 10, None), 14)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 10, 11, None), 14)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 10, 12, None), 14)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 10, 13, None), 14)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 10, 14, None), 14)

        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 11, 10, None), 14)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 11, 11, None), 14)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 11, 12, None), 14)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 11, 13, None), 14)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 11, 14, None), 14)

        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 12, 10, None), 14)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 12, 11, None), 14)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 12, 12, None), 14)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 12, 13, None), 14)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 12, 14, None), 14)

        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 13, 10, None), 14)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 13, 11, None), 14)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 13, 12, None), 14)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 13, 13, None), 14)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 13, 14, None), 14)

    def test__adjust_right__4(self):
        #          00000000001111
        #          01234567890123
        #          .  |<
        pattern = "*** **** *****"
        rng = {'B': (4, 8), 'C': (8, 14)}
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 0, 2, rng), 3)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 0, 3, rng), 3)

    def test__adjust_right__5(self):
        #          00000000001111
        #          01234567890123
        #          .       |<
        pattern = "*******  *****"
        rng = {'C': (9, 14)}
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 0, 2, rng), 8)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 0, 3, rng), 8)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_right(pattern, 0, 10, rng), 14)

    def test__adjust_left__1(self):
        #          00000000001111
        #          01234567890123
        #         >|  .
        pattern = "*** **** *****"
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 0, 1, None), 0)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 0, 2, None), 0)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 0, 3, None), 0)

        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 1, 1, None), 0)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 1, 2, None), 0)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 1, 3, None), 0)

        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 2, 1, None), 0)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 2, 2, None), 0)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 2, 3, None), 0)

    def test__adjust_left__2(self):
        #          00000000001111
        #          01234567890123
        #             >|   .
        pattern = "*** **** *****"
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 4, 5, None), 4)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 4, 6, None), 4)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 4, 7, None), 4)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 4, 8, None), 4)

        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 5, 5, None), 4)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 5, 6, None), 4)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 5, 7, None), 4)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 5, 8, None), 4)

        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 6, 5, None), 4)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 6, 6, None), 4)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 6, 7, None), 4)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 6, 8, None), 4)

        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 7, 5, None), 4)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 7, 6, None), 4)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 7, 7, None), 4)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 7, 8, None), 4)

    def test__adjust_left__3(self):
        #          00000000001111
        #          01234567890123
        #                  >|    .
        pattern = "*** **** *****"
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 9, 10, None), 9)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 9, 11, None), 9)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 9, 12, None), 9)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 9, 13, None), 9)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 9, 14, None), 9)

        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 10, 10, None), 9)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 10, 11, None), 9)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 10, 12, None), 9)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 10, 13, None), 9)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 10, 14, None), 9)

        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 11, 10, None), 9)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 11, 11, None), 9)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 11, 12, None), 9)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 11, 13, None), 9)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 11, 14, None), 9)

        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 12, 10, None), 9)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 12, 11, None), 9)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 12, 12, None), 9)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 12, 13, None), 9)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 12, 14, None), 9)

        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 13, 10, None), 9)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 13, 11, None), 9)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 13, 12, None), 9)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 13, 13, None), 9)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 13, 14, None), 9)

    def test__adjust_left__4(self):
        #          00000000001111
        #          01234567890123
        #         >|  .
        pattern = "*** **** *****"
        rng = {'B': (4, 8), 'C': (8, 14)}
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 0, 2, rng), 0)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 0, 3, rng), 0)

    def test__adjust_left__5(self):
        #          00000000001111
        #          01234567890123
        #          (      )|<
        pattern = "*******  *****"
        rng = {'A': (0, 7)}
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 9, 14, rng), 8)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 12, 14, rng), 8)
        self.assertEqual(fdiskparser_.FdiskParser._adjust_left(pattern, 7, 10, rng), 0)

if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
