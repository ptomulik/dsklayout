#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import unittest.mock as mock

import dsklayout.cli.dsklayout_ as dsklayout_
import dsklayout.cli.app_ as app_
import dsklayout.cli.backupcmd_ as backupcmd_

from dsklayout import __version__ as dsklayout_version

class Test__DskLayout(unittest.TestCase):

    def test__isinstance_main(self):
        app = dsklayout_.DskLayout()
        self.assertIsInstance(app, app_.CliApp)

    def test__properties(self):
        app = dsklayout_.DskLayout()
        self.assertEqual(app.properties, {
            'description': 'Retrieve and backup layouts of block devices'
        })

    def test__version(self):
        app = dsklayout_.DskLayout()
        self.assertEqual(app.version, dsklayout_version)

    def test__subcommands(self):
        app = dsklayout_.DskLayout()
        self.assertEqual(app.subcommands, [
            backupcmd_.CliBackupCmd
        ])

    def test__add_arguments(self):
        parser = mock.Mock(spec = [])
        parser.add_argument = mock.Mock()
        app = dsklayout_.DskLayout()
        self.assertIsNone(app.add_arguments(parser))
        parser.add_argument.assert_called_once_with('-v', '--version',
                action='version', version=('%(prog)s ' + app.version) )

    def test__set_defaults(self):
        parser = mock.Mock(spec = [])
        app = dsklayout_.DskLayout()
        self.assertIsNone(app.set_defaults(parser))


if __name__ == '__dsklayout__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
