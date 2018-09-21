#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
from unittest.mock import patch
import dsklayout.cli as cli

class Test__cli__PackageSymbols(unittest.TestCase):

    def test__clibackupcmd__symbols(self):
        self.assertIs(cli.CliBackupCmd, cli.backupcmd_.CliBackupCmd)

    def test__clidotcmd__symbols(self):
        self.assertIs(cli.CliDotCmd, cli.dotcmd_.CliDotCmd)

    def test__clicmd__symbols(self):
        self.assertIs(cli.CliCmd, cli.cmd_.CliCmd)

    def test__clicmdbase__symbols(self):
        self.assertIs(cli.CliCmdBase, cli.cmdbase_.CliCmdBase)

    def test__cliext__symbols(self):
        self.assertIs(cli.CliExt, cli.ext_.CliExt)

    def test__dsklayout__symbols(self):
        self.assertIs(cli.DskLayout, cli.dsklayout_.DskLayout)

    def test__app__symbols(self):
        self.assertIs(cli.CliApp, cli.app_.CliApp)

class Test__main(unittest.TestCase):

    def test__main__0(self):
        with patch.object(cli.DskLayout, 'run', return_value='ok') as run:
            result = cli.main()
            run.assert_called_once_with()
            self.assertEqual('ok', result)

    def test__main__Exception(self):
        with patch.object(cli.DskLayout, 'run', side_effect=RuntimeError('foo')) as run:
            with self.assertRaises(RuntimeError) as context:
                cli.main()
            self.assertEqual('foo', str(context.exception))

    def test__main__KeyboardInterrupt(self):
        with patch.object(cli.DskLayout, 'run', side_effect=KeyboardInterrupt()) as run:
            result = cli.main()
            run.assert_called_once_with()
            self.assertIs(0, result)

if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
