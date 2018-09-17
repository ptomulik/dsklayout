# -*- coding: utf8 -*-
"""Provides the CliCmdBase class
"""

import abc

__all__ = ('CliCmdBase',)


class CliCmdBase(metaclass=abc.ABCMeta):
    """An abstract base class for either command or command extension.

    Intended to be inherited by CliCmd and CliExt classes.
    """

    @property
    @abc.abstractmethod
    def name(self):
        """Name of the command or command extension

        .. note:: This property **must** be implemented in a subclass.
        """
        pass

    def add_arguments(self, parser):
        """Adds command's argument definitions to argument parser

        :param argparse.ArgumentParser parser: the target argument parser to be
                                               modified

        .. note::
                A subclass may reimplement this method to define custom
                command-line arguments.
        """
        pass

    def set_defaults(self, parser):
        """Sets defaults to this command's arguments parser

        :param argparse.ArgumentParser parser: the target argument parser to be
                                               modified

        .. note::
                A subclass may reimplement this method to provide custom
                defaults to certain command-line arguments.
        """
        pass

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
