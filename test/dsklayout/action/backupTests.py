#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import unittest.mock as mock

import dsklayout.action.backup_ as backup_
import dsklayout.action.action_ as action_


class Test__BackupAction(unittest.TestCase):

    def test__issubclass__Action(self):
        self.assertTrue(issubclass(backup_.BackupAction, action_.Action))

##    def test__call__(self):
##        subject = mock.Mock()
##        action = TestAction('foo')
##        self.assertEqual(action(subject), (subject, 'foo'))


if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
