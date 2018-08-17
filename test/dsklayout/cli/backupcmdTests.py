#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import unittest.mock as mock

import dsklayout.cli.backupcmd_ as backupcmd_
import dsklayout.cli.cmd_ as cmd_

class Test__CliBackupCmd(unittest.TestCase):

    def test__isinstance_clicmd(self):
        cmd = backupcmd_.CliBackupCmd()
        self.assertIsInstance(cmd, cmd_.CliCmd)

    def test__name(self):
        cmd = backupcmd_.CliBackupCmd()
        self.assertEqual(cmd.name, 'backup')

    def test__properties(self):
        cmd = backupcmd_.CliBackupCmd()
        self.assertEqual(cmd.properties, {'description': 'backup disk layout'})

    def test__add_cmd_arguments(self):
        cmd = backupcmd_.CliBackupCmd()
        parser = mock.Mock(spec =[])
        parser.add_argument = mock.Mock()
        self.assertIsNone(cmd.add_cmd_arguments(parser))
        parser.add_argument.assert_has_calls([
            mock.call("devices", metavar='DEV', nargs="*",
                      help="block device to be included in backup")
        ])

    @unittest.skip("test not implemented yet!")
    def test__run(self):
        self.assertTrue(False)
        #cmd = backupcmd_.CliBackupCmd()
        #self.assertEqual(cmd.run(), 0)

if __name__ == '__backupcmd__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
