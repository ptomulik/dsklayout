# -*- coding: utf8 -*-
"""Provides the CliCmdBase class
"""

import abc

__all__ = ('CliCmdBase',)


class CliCmdBase(object, metaclass=abc.ABCMeta):
    """An abstract base class for either command or command extension.

    Intended to be inherited by CliCmd and CliExt classes.
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
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
