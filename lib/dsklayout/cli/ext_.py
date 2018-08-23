# -*- coding: utf8 -*-
"""Provides the CliExt class
"""

from . import cmdbase_

__all__ = ('CliExt',)


class CliExt(cmdbase_.CliCmdBase):
    """A base class for CLI extensions."""

    __slots__ = ('_parent',)

    @property
    def parent(self):
        """A parent command which contains this extension"""
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def arguments(self):
        """Arguments provided via command-line"""
        return self._parent.arguments

    def add_arguments(self, parser):
        """Add extension's argument definitions to an argument parser

        :note: This method **shall** be customized in a subclass

        :param argparse.ArgumentParser parser: the destination parser object
                                               for the arguments.
        """
        pass

    def set_defaults(self, parser):
        """Sets extension's defaults to an argument parser

        :note: This method **may** be customized in a subclass

        :param argparse.ArgumentParser parser: the destination parser object
                                               for the argument defaults.
        """
        pass

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
