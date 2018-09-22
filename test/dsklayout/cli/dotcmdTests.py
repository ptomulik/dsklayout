#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import unittest.mock as mock
import argparse

import dsklayout.cli.dotcmd_ as dotcmd_
import dsklayout.cli.cmd_ as cmd_
import dsklayout.cli.progext_ as progext_
import dsklayout.cli.tmpdirext_ as tmpdirext_

class Test__CliDotCmd(unittest.TestCase):

    def test__isinstance_clicmd(self):
        cmd = dotcmd_.CliDotCmd()
        self.assertIsInstance(cmd, cmd_.CliCmd)

    def test__name(self):
        cmd = dotcmd_.CliDotCmd()
        self.assertEqual(cmd.name, 'dot')

    def test__properties(self):
        cmd = dotcmd_.CliDotCmd()
        self.assertEqual(cmd.properties, {'description': 'generate graph representation of disk layout'})

    def test__add_cmd_arguments(self):
        cmd = dotcmd_.CliDotCmd()
        parser = mock.Mock(spec =[])
        parser.add_argument = mock.Mock()
        self.assertIsNone(cmd.add_cmd_arguments(parser))
        parser.add_argument.assert_has_calls([
            mock.call("--view", action='store_true', help="display graph instead of writting its source"),
            mock.call("-o", "--output", metavar='FILE', help="write output to FILE instead of stdout"),
            mock.call("-i", "--input", metavar='FILE', help="use FILE as input instead of probing OS, FILE should be an archive previously created with dsklayout backup"),
            mock.call("devices", metavar='DEV', nargs="*", help="top-level block devices to be included in graph")
        ])

    def test__extensions__01(self):
        cmd = dotcmd_.CliDotCmd()
        self.assertIsInstance(cmd.extensions['lsblk'], progext_.ProgExt)

    def test__extensions__02(self):
        cmd = dotcmd_.CliDotCmd()
        self.assertIs(cmd.extensions['lsblk'], cmd.lsblk)

    def test__run(self):
        cmd = dotcmd_.CliDotCmd()
        cmd.arguments = argparse.Namespace()
        with mock.patch.object(dotcmd_.DotCmd, 'run', return_value='ok') as run:
            self.assertEqual('ok', cmd.run())
            run.assert_called_once_with()

if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
