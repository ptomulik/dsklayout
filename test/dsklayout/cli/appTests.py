#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import unittest.mock as mock
import argparse

import dsklayout.cli.app_ as app_

class Test__App(unittest.TestCase):

    def test__init__(self):
        parser = mock.Mock()
        subparsers = mock.Mock()
        parser.add_subparsers = mock.Mock(return_value = subparsers)
        with mock.patch.object(app_.App, 'add_arguments') as add_arguments, \
             mock.patch.object(app_.App, 'set_defaults') as set_defaults, \
             mock.patch.object(app_.App, 'add_subcommands') as add_subcommands, \
             mock.patch.object(argparse, 'ArgumentParser', return_value = parser) as ArgumentParser:
            main = app_.App()
            self.assertIs(main.parser, parser)
            self.assertIs(main.subparsers, subparsers)
            add_arguments.assert_called_once_with(parser)
            set_defaults.assert_called_once_with(parser)
            add_subcommands.assert_called_once_with(subparsers)

    def test__parser(self):
        main = app_.App()
        self.assertIsInstance(main.parser, argparse.ArgumentParser)

    def test__subparsers(self):
        main = app_.App()
        self.assertIsNotNone(main.subparsers)
        self.assertTrue(hasattr(main.subparsers, 'add_parser'))

    def test__properties(self):
        self.assertEqual(app_.App().properties, dict())

    def test__subproperties(self):
        main = app_.App()
        self.assertEqual(main.subproperties['title'], 'commands')

    def test__subcommands(self):
        self.assertEqual(app_.App().subcommands, [])

    def test__add_arguments(self):
        parser = mock.Mock()
        self.assertIsNone(app_.App().add_arguments(parser))

    def test__set_defaults(self):
        parser = mock.Mock()
        self.assertIsNone(app_.App().set_defaults(parser))

    def test__add_subcommands(self):
        cmd_instance = mock.Mock()
        cmd_klass = mock.Mock(return_value = cmd_instance)
        subparsers = mock.Mock()
        main = app_.App()
        with mock.patch.object(app_.App, 'add_subcommand') as add_subcommand, \
             mock.patch.object(app_.App, 'subcommands', [cmd_klass]):
                 self.assertIsNone(main.add_subcommands(subparsers))
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

        main = app_.App()
        self.assertIsNone(main.add_subcommand(subparsers, command))
        subparsers.add_parser.assert_called_once_with(command.name, **command.properties)
        command.add_arguments.assert_called_once_with(subparser1)
        command.set_defaults.assert_called_once_with(subparser1)
        subparser1.set_defaults.assert_called_once_with(command=command)

    def test__run(self):
        main = app_.App()
        arguments = mock.Mock()
        arguments.command = mock.Mock()
        arguments.command.run = mock.Mock(return_value = 'ok')
        with mock.patch.object(app_.App, 'parser') as parser, \
             mock.patch('sys.argv', ['prog','arg1','arg2']) as argv:
            parser.parse_args = mock.Mock(return_value = arguments)
            main = app_.App()
            self.assertEqual(main.run(), 'ok')
            parser.parse_args.assert_called_once_with(argv[1:])
            arguments.command.run.assert_called_once_with()

    def test__run__without_command(self):
        main = app_.App()
        arguments = mock.Mock(spec=[])
        with mock.patch.object(app_.App, 'parser') as parser, \
             mock.patch('sys.argv', ['prog','arg1','arg2']) as argv:
            parser.parse_args = mock.Mock(return_value = arguments)
            parser.print_help = mock.Mock(return_value = 'ok')
            main = app_.App()
            self.assertEqual(main.run(), 'ok')
            parser.parse_args.assert_called_once_with(argv[1:])
            parser.print_help.assert_called_once_with()

if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
