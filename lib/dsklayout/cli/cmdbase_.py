# -*- coding: utf8 -*-
"""Provides the CmdBase class
"""

import abc

__all__ = ('CmdBase',)


class CmdBase(object, metaclass=abc.ABCMeta):
    """An abstract base class for either command or command extension.

    Intended to be inherited by Cmd and CmdExt classes.
    """

    @property
    @abc.abstractmethod
    def name(self):
        pass

    def add_arguments(self, parser):
        """Adds command's argument definitions to argument parser"""
        pass

    def set_defaults(self, parser):
        """Sets defaults to this command's arguments parser"""
        pass

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
