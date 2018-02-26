# -*- coding: utf8 -*-
"""Provides the CmdExt class
"""

from . import cmdbase_

__all__ = ('CmdExt',)


class CmdExt(cmdbase_.CmdBase):

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
        """Add extension's argument definitions to an argument parser"""
        pass

    def set_defaults(self, parser):
        """Sets extension's defaults to an argument parser"""
        pass

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
