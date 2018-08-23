# -*- coding: utf8 -*-
"""Provides the ProgExt class
"""

from . import ext_

__all__ = ('ProgExt',)


class ProgExt(ext_.CliExt):
    """A CLI extension defining an external program (custom path).

    The :class:`.ProgExt` object defines a CLI option for a program. This
    allows user to pass program's custom name or path to our CLI application.
    """

    __slots__ = ('_name', '_properties')

    def __init__(self, name, **kw):
        """
        :param str name: name of the extension,
        :keyword str prog_option: option name (e.g. ``"--foo-bar"``),
        :keyword str prog_dest: option destination (e.g. ``"foo_bar"``),
        :keyword str prog_default: default program name/path,
        :keyword str prog_help: help for the program option,
        :keyword str prog_name: program name.
        """
        super().__init__()
        keys = ('prog_option', 'prog_dest', 'prog_default', 'prog_help',
                'prog_name')
        self._name = name
        self._properties = {k: kw[k] for k in kw if k in keys}

    @property
    def name(self):
        """Name of this extension."""
        return self._name

    @property
    def prog_option(self):
        """Name of the CLI option providing the program path."""
        return self._get('prog_option', '--%s' % self.name)

    @property
    def prog_dest(self):
        """Name of argparse attribute storing the program path."""
        return self._get('prog_dest', self.name)

    @property
    def prog_default(self):
        """Default value of the program option."""
        return self._get('prog_default', self.name)

    @property
    def prog_help(self):
        """Help for the program option."""
        return self._get('prog_help', 'path to %s program' % self.prog_name)

    @property
    def prog_name(self):
        """Name of the program."""
        return self._get('prog_name', self.name)

    def add_arguments(self, parser):
        """Add extension's argument definitions to an argument parser.

        :param argparse.ArgumentParser parser: the destination parser object
                                               for the arguments.
        """
        self.add_prog_argument(parser)

    def add_prog_argument(self, parser):
        """Add the program argument to argparse object.

        :param argparse.ArgumentParser parser: the target parser object.
        """
        parser.add_argument(self.prog_option,
                            dest=self.prog_dest,
                            metavar="PROG",
                            default=self.prog_default,
                            help=self.prog_help)

    def _get(self, key, default=None):
        return self._properties.get(key, default)


# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
