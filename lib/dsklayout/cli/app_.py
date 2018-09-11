# -*- coding: utf8 -*-
"""Provides the CliApp class
"""

from . import backupcmd_

import argparse
import sys

__all__ = ('CliApp',)


class CliApp:
    """Abstract base class for a command-line application"""

    __slots__ = ('_parser', '_subparsers')

    def __init__(self):
        self._parser = argparse.ArgumentParser(**self.properties)
        self._subparsers = self._parser.add_subparsers(**self.subproperties)
        self.add_arguments(self._parser)
        self.set_defaults(self._parser)
        self.add_subcommands(self._subparsers)

    @property
    def parser(self):
        """CLI argument parser

        :rtype: argparse.ArgumentParser
        """
        return self._parser

    @property
    def subparsers(self):
        """CLI argument subparsers

        :rtype: list(argparse.ArgumentParser)
        """
        return self._subparsers

    @property
    def properties(self):
        """Properties used when creating argument parser

        :rtype: dict
        """
        return dict()

    @property
    def subproperties(self):
        """Properties used when creating subparsers object

        :rtype: dict
        """
        return {'title':  'commands'}

    @property
    def subcommands(self):
        """A list of classes implementing our subcommands

        :rtype: list
        """
        return []

    @property
    def version(self):
        return '(unknown version)'

    def add_arguments(self, parser):
        """Add common arguments (not specific to any subcommand)."""
        parser.add_argument('-v', '--version', action='version',
                            version=('%(prog)s ' + self.version))

    def set_defaults(self, parser):
        pass

    def add_subcommands(self, subparsers):
        for klass in self.subcommands:
            self.add_subcommand(subparsers, klass())

    def add_subcommand(self, subparsers, command):
        """Add subcommand"""
        subparser = subparsers.add_parser(command.name, **command.properties)
        command.add_arguments(subparser)
        command.set_defaults(subparser)
        subparser.set_defaults(command=command)

    def run(self):
        """Run subcommand"""
        arguments = self.parser.parse_args(sys.argv[1:])
        try:
            command = arguments.command
        except AttributeError:
            return self.parser.print_help()
        command.arguments = arguments
        return command.run()


# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
