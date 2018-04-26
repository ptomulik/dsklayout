#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import unittest.mock as mock

import dsklayout.cli.dsklayout_ as dsklayout_
import dsklayout.cli.app_ as app_
import dsklayout.cli.backupcmd_ as backupcmd_

class Test__DskLayout(unittest.TestCase):

    def test__isinstance_main(self):
        app = dsklayout_.DskLayout()
        self.assertIsInstance(app, app_.CliApp)

    def test__properties(self):
        app = dsklayout_.DskLayout()
        self.assertEqual(app.properties, {
            'description': 'Retrieve and backup layouts of block devices'
        })

    def test__subcommands(self):
        app = dsklayout_.DskLayout()
        self.assertEqual(app.subcommands, [
            backupcmd_.CliBackupCmd
        ])

    def test__add_arguments(self):
        parser = mock.Mock(spec = [])
        app = dsklayout_.DskLayout()
        self.assertIsNone(app.add_arguments(parser))

    def test__set_defaults(self):
        parser = mock.Mock(spec = [])
        app = dsklayout_.DskLayout()
        self.assertIsNone(app.set_defaults(parser))


if __name__ == '__dsklayout__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
