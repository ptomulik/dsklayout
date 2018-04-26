#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import dsklayout.cli as cli

class Test__cli__PackageSymbols(unittest.TestCase):

    def test__backupcmd__symbols(self):
        self.assertIs(cli.CliBackupCmd, cli.backupcmd_.CliBackupCmd)

    def test__main__symbols(self):
        self.assertIs(cli.CliCmd, cli.cmd_.CliCmd)

    def test__cmdbase__symbols(self):
        self.assertIs(cli.CliCmdBase, cli.cmdbase_.CliCmdBase)

    def test__cmdext__symbols(self):
        self.assertIs(cli.CliExt, cli.ext_.CliExt)

    def test__dsklayout__symbols(self):
        self.assertIs(cli.DskLayout, cli.dsklayout_.DskLayout)

    def test__lsblkext__symbols(self):
        self.assertIs(cli.LsBlkExt, cli.lsblkext_.LsBlkExt)

    def test__app__symbols(self):
        self.assertIs(cli.CliApp, cli.app_.CliApp)

if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
