#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import dsklayout.cli as cli

class Test__cli__PackageSymbols(unittest.TestCase):

    def test__backupcmd__symbols(self):
        self.assertIs(cli.BackupCmd, cli.backupcmd_.BackupCmd)

    def test__main__symbols(self):
        self.assertIs(cli.Cmd, cli.cmd_.Cmd)

    def test__cmdbase__symbols(self):
        self.assertIs(cli.CmdBase, cli.cmdbase_.CmdBase)

    def test__cmdext__symbols(self):
        self.assertIs(cli.CmdExt, cli.cmdext_.CmdExt)

    def test__dsklayout__symbols(self):
        self.assertIs(cli.DskLayout, cli.dsklayout_.DskLayout)

    def test__lsblkext__symbols(self):
        self.assertIs(cli.LsBlkExt, cli.lsblkext_.LsBlkExt)

    def test__app__symbols(self):
        self.assertIs(cli.CliApp, cli.app_.CliApp)

if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
