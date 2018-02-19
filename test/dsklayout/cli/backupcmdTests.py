#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import unittest.mock as mock

import dsklayout.cli.backupcmd_ as backupcmd_
import dsklayout.cli.cmd_ as cmd_

class Test__BackupCmd(unittest.TestCase):

    def test__isinstance_cmd(self):
        cmd = backupcmd_.BackupCmd()
        self.assertIsInstance(cmd, cmd_.Cmd)

    def test__name(self):
        cmd = backupcmd_.BackupCmd()
        self.assertEqual(cmd.name, 'backup')

    def test__properties(self):
        cmd = backupcmd_.BackupCmd()
        self.assertEqual(cmd.properties, {'description': 'backup disk layout'})

    def test__add_cmd_arguments(self):
        cmd = backupcmd_.BackupCmd()
        parser = mock.Mock(spec =[])
        parser.add_argument = mock.Mock()
        self.assertIsNone(cmd.add_cmd_arguments(parser))
        parser.add_argument.assert_has_calls([
            mock.call("devices", metavar='DEV', nargs="*",
                      help="block device to be included in backup")
        ])

    def test__run(self):
        cmd = backupcmd_.BackupCmd()
        self.assertEqual(cmd.run(), 0)

if __name__ == '__backupcmd__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
