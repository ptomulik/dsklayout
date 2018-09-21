#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import unittest.mock as mock
import argparse

import dsklayout.cli.app_ as app_

class Test__CliApp(unittest.TestCase):

    def test__init__(self):
        parser = mock.Mock()
        subparsers = mock.Mock()
        parser.add_subparsers = mock.Mock(return_value = subparsers)
        with mock.patch.object(app_.CliApp, 'add_arguments') as add_arguments, \
             mock.patch.object(app_.CliApp, 'set_defaults') as set_defaults, \
             mock.patch.object(app_.CliApp, 'add_subcommands') as add_subcommands, \
             mock.patch.object(argparse, 'ArgumentParser', return_value = parser) as ArgumentParser:
            app = app_.CliApp()
            self.assertIs(app.parser, parser)
            self.assertIs(app.subparsers, subparsers)
            add_arguments.assert_called_once_with(parser)
            set_defaults.assert_called_once_with(parser)
            add_subcommands.assert_called_once_with(subparsers)

    def test__parser(self):
        app = app_.CliApp()
        self.assertIsInstance(app.parser, argparse.ArgumentParser)

    def test__subparsers(self):
        app = app_.CliApp()
        self.assertIsNotNone(app.subparsers)
        self.assertTrue(hasattr(app.subparsers, 'add_parser'))

    def test__properties(self):
        self.assertEqual(app_.CliApp().properties, dict())

    def test__subproperties(self):
        app = app_.CliApp()
        self.assertEqual(app.subproperties['title'], 'commands')

    def test__subcommands(self):
        self.assertEqual(app_.CliApp().subcommands, [])

    def test__version(self):
        self.assertEqual(app_.CliApp().version, '(unknown version)')

    def test__add_arguments(self):
        parser = mock.Mock()
        self.assertIsNone(app_.CliApp().add_arguments(parser))

    def test__set_defaults(self):
        parser = mock.Mock()
        self.assertIsNone(app_.CliApp().set_defaults(parser))

    def test__add_subcommands(self):
        cmd_instance = mock.Mock()
        cmd_klass = mock.Mock(return_value = cmd_instance)
        subparsers = mock.Mock()
        app = app_.CliApp()
        with mock.patch.object(app_.CliApp, 'add_subcommand') as add_subcommand, \
             mock.patch.object(app_.CliApp, 'subcommands', [cmd_klass]):
                 self.assertIsNone(app.add_subcommands(subparsers))
                 add_subcommand.assert_called_once_with(subparsers, cmd_instance)


    def test__add_subcommand(self):
        subparsers = mock.Mock()
        subparser1 = mock.Mock()
        subparser1.set_defaults = mock.Mock()
        subparsers.add_parser = mock.Mock(return_value = subparser1)
        command = mock.Mock()
        command.name = 'cmd'
        command.properties = dict()
        command.add_arguments = mock.Mock()
        command.set_defaults = mock.Mock()

        app = app_.CliApp()
        self.assertIsNone(app.add_subcommand(subparsers, command))
        subparsers.add_parser.assert_called_once_with(command.name, **command.properties)
        command.add_arguments.assert_called_once_with(subparser1)
        command.set_defaults.assert_called_once_with(subparser1)
        subparser1.set_defaults.assert_called_once_with(command=command)

    def test__run(self):
        app = app_.CliApp()
        arguments = mock.Mock()
        arguments.command = mock.Mock()
        arguments.command.run = mock.Mock(return_value = 'ok')
        with mock.patch.object(app_.CliApp, 'parser') as parser, \
             mock.patch('sys.argv', ['prog','arg1','arg2']) as argv:
            parser.parse_args = mock.Mock(return_value = arguments)
            app = app_.CliApp()
            self.assertEqual(app.run(), 'ok')
            parser.parse_args.assert_called_once_with(argv[1:])
            arguments.command.run.assert_called_once_with()

    def test__run__without_command(self):
        app = app_.CliApp()
        arguments = mock.Mock(spec=[])
        with mock.patch.object(app_.CliApp, 'parser') as parser, \
             mock.patch('sys.argv', ['prog','arg1','arg2']) as argv:
            parser.parse_args = mock.Mock(return_value = arguments)
            parser.print_help = mock.Mock(return_value = 'ok')
            app = app_.CliApp()
            self.assertEqual(app.run(), 'ok')
            parser.parse_args.assert_called_once_with(argv[1:])
            parser.print_help.assert_called_once_with()

if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
