# -*- coding: utf8 -*-
"""Provides the CliApp class
"""

from . import backupcmd_

import argparse
import sys

__all__ = ('CliApp',)


class CliApp:
    """Abstract base class for a command-line application.

    A typical application shall inherit this class and reimplement
    :attr:`.properties`, :attr:`.subcommands` and :attr:`.version`.
    The default implementation of :meth:`.run` is just a dispatcher, which
    dispatches control to appropriate subcommand.
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
        """CLI argument parser.

        This is the main argument parser used by application. All the
        :attr:`.subparsers` are attached to :attr:`.parser`.

        :rtype: argparse.ArgumentParser
        """
        return self._parser

    @property
    def subparsers(self):
        """CLI argument subparsers.

        Subparsers are argument parsers provided by subcommands. They're used
        to parse subcommand-specific command-line options.

        .. note::
                There is no need to override this property. The list is filled
                automatically when consecutive subcommands are added during
                :class:`.CliApp` construction.

        :rtype: list(argparse.ArgumentParser)
        """
        return self._subparsers

    @property
    def properties(self):
        """Properties used when creating argument parser.

        These properties are passed as keyword arguments to the constructor of
        :class:`argparse.ArgumentParser` when creating :attr:`.parser`.

        .. note::
                A subclass may redefine this property to provide custom
                keyword arguments to the constructor when :attr:`.parser`
                is being created.

        :rtype: dict
        """
        return dict()

    @property
    def subproperties(self):
        """Properties used when creating :attr:`.subparsers` object.

        .. note::
                A subclass may override this property to provide keyword
                arguments to
                :meth:`argparse.ArgumentParser.add_subparsers`
                when the container for subparsers is created.

        :rtype: dict
        """
        return {'title':  'commands'}

    @property
    def subcommands(self):
        """A list of classes implementing application's subcommands.

        .. note::
                The default list is empty. A subclass shall override this
                property to provide actual list of subcommands. All entries
                shall be subclasses of :class:`.CliCmd`.

        :rtype: list(type)
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
        """Add argument definitions to **parser**.


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
        """Set defaults to application command-line options.

        :param argparse.ArgumentParser parser: target argument parser to be
                                               modified.

        .. note::

                A subclass may reimplement this method to provide custom
                defaults to application's arguments.
        """
        pass

    def run(self):
        """Execute application.

        This is the main entry point to the application. The default
        implementation parses command-line arguments and invokes appropriate
        subcommand by calling its ``run()`` method. If the command-line
        arguments are invalid, a help message is printed.


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
        """Add single subcommand."""
        subparser = subparsers.add_parser(command.name, **command.properties)
        command.add_arguments(subparser)
        command.set_defaults(subparser)
        subparser.set_defaults(command=command)


# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
