# -*- coding: utf8 -*-
"""Provides the CliApp class
"""

from . import backupcmd_

import argparse
import sys

__all__ = ('CliApp',)


class CliApp:
    """Abstract base class for a command-line application

    A typical application shall inherit this class and reimplement
    :attr:`.properties`, :attr:`.subcommands` and :attr:`.version`.
    """

    __slots__ = ('_parser', '_subparsers')

    def __init__(self):
        self._parser = argparse.ArgumentParser(**self.properties)
        self._subparsers = self._parser.add_subparsers(**self.subproperties)
        self.add_arguments(self._parser)
        self.set_defaults(self._parser)
        self._add_subcommands(self._subparsers)

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
        """Application version

        .. note::

            This property shall be implemented in a subclass.

        :returns: application version
        :rtype: str
        """
        return '(unknown version)'

    def add_arguments(self, parser):
        """Add common arguments (not specific to any subcommand) to an argument
        parser


        :param argparse.ArgumentParser parser: argument parser, where the
                                               options will be registered

        The default implementation implements ``-v, --version`` option, which
        just displays a string returned by :attr:`.version` property.

        .. note::
                A subclass may overwrite this method to define extra
                command-line arguments.

        .. note::
                ``-h, --help`` is provided by :class:`argparse.ArgumentParser`;
                there is no need to define it explicitly.
        """
        parser.add_argument('-v', '--version', action='version',
                            version=('%(prog)s ' + self.version))

    def set_defaults(self, parser):
        """Set defaults for application command-line options

        :param argparse.ArgumentParser parser: Argument parser with
                                               application's arguments.

        .. note::

                A subclass may reimplement this method to provide custom
                defaults to application's arguments.
        """
        pass

    def run(self):
        """Run subcommand

        Main entry point to the application. The default implementation parses
        command-line arguments and invokes appropriate subcommand's ``run()``
        method.

        :returns: status code returned by the subcommand.
        :rtype: int
        """
        arguments = self.parser.parse_args(sys.argv[1:])
        try:
            command = arguments.command
        except AttributeError:
            return self.parser.print_help()
        command.arguments = arguments
        return command.run()

    def _add_subcommands(self, subparsers):
        """Add all subcommands defined by :attr:`.subcommands`."""
        for klass in self.subcommands:
            self._add_subcommand(subparsers, klass())

    def _add_subcommand(self, subparsers, command):
        """Add single subcommand"""
        subparser = subparsers.add_parser(command.name, **command.properties)
        command.add_arguments(subparser)
        command.set_defaults(subparser)
        subparser.set_defaults(command=command)


# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
