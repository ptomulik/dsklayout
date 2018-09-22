#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import unittest.mock as mock
import argparse

import dsklayout.cli.backupcmd_ as backupcmd_
import dsklayout.cli.cmd_ as cmd_
import dsklayout.cli.progext_ as progext_
import dsklayout.cli.tmpdirext_ as tmpdirext_

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
            mock.call("outfile", metavar='OUTFILE', help="output file"),
            mock.call("devices", metavar='DEV', nargs="*", help="block device to be included in backup")
        ])

    def test__extensions__01(self):
        cmd = backupcmd_.CliBackupCmd()
        self.assertIsInstance(cmd.extensions['lsblk'], progext_.ProgExt)
        self.assertIsInstance(cmd.extensions['fdisk'], progext_.ProgExt)
        self.assertIsInstance(cmd.extensions['sfdisk'], progext_.ProgExt)
        self.assertIsInstance(cmd.extensions['sgdisk'], progext_.ProgExt)
        self.assertIsInstance(cmd.extensions['mdadm'], progext_.ProgExt)
        self.assertIsInstance(cmd.extensions['vgcfgbackup'], progext_.ProgExt)
        self.assertIsInstance(cmd.extensions['pvs'], progext_.ProgExt)
        self.assertIsInstance(cmd.extensions['vgs'], progext_.ProgExt)
        self.assertIsInstance(cmd.extensions['lvs'], progext_.ProgExt)
        self.assertIsInstance(cmd.extensions['tmpdir'], tmpdirext_.TmpDirExt)

    def test__extensions__02(self):
        cmd = backupcmd_.CliBackupCmd()
        self.assertIs(cmd.extensions['lsblk'], cmd.lsblk)
        self.assertIs(cmd.extensions['fdisk'], cmd.fdisk)
        self.assertIs(cmd.extensions['sfdisk'], cmd.sfdisk)
        self.assertIs(cmd.extensions['sgdisk'], cmd.sgdisk)
        self.assertIs(cmd.extensions['mdadm'], cmd.mdadm)
        self.assertIs(cmd.extensions['vgcfgbackup'], cmd.vgcfgbackup)
        self.assertIs(cmd.extensions['pvs'], cmd.pvs)
        self.assertIs(cmd.extensions['vgs'], cmd.vgs)
        self.assertIs(cmd.extensions['lvs'], cmd.lvs)
        self.assertIs(cmd.extensions['tmpdir'], cmd.tmpdir)

    def test__run(self):
        cmd = backupcmd_.CliBackupCmd()
        cmd.arguments = argparse.Namespace()
        with mock.patch.object(backupcmd_.BackupCmd, 'run', return_value='ok') as run:
            self.assertEqual('ok', cmd.run())
            run.assert_called_once_with()

if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
