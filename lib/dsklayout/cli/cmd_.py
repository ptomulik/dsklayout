# -*- coding: utf8 -*-
"""Provides the CliCmd class
"""

from . import cmdbase_

__all__ = ('CliCmd',)


class CliCmd(cmdbase_.CliCmdBase):
    """Base class for actual command (subcommand)"""

    __slots__ = ('_arguments', '_extensions')

    def __init__(self, **kw):
        super().__init__()
        self._extensions = kw.get('extensions', dict())

    @property
    def extensions(self):
        """A list of extensions used by this subcommand.

        :rtype: list(CliExt)
        """
        return self._extensions

    @property
    def properties(self):
        """Properties used when creating an instance of
        :class:`argparse.ArgumentParser` for this subcommand.

        .. note::
                A subclass may overwrite this property.

        :rtype: dict
        """
        return dict()

    @property
    def arguments(self):
        """Arguments with their values provided by user.

        :rtype: argparse.Namespace
        """
        return self._arguments

    @arguments.setter
    def arguments(self, arguments):
        """Setter for :attr:`.arguments`"""
        self._arguments = arguments

    def __getattr__(self, name):
        try:
            return self._extensions[name]
        except KeyError:
            raise AttributeError(name)

    def add_extension(self, ext, name=None):
        """Add an extension to this subcommand

        :param .CliExt ext: an extension object to be added,
        :param str name: custom name (if different from extension-provided name).

        .. note::
                This method shall be invoked from subclass's constructor.
        """
        if name is None:
            name = ext.name
        self._extensions[name] = ext
        ext.parent = self

    def add_arguments(self, parser):
        """Custom implementation of :meth:`.CliCmdBase.add_arguments`.

        This method just invokes :meth:`.add_cmd_arguments` and
        :meth:`.add_ext_arguments`.
        """
        self.add_cmd_arguments(parser)
        self.add_ext_arguments(parser)

    def add_ext_arguments(self, parser):
        """Add arguments defined by our extensions

        :param argparse.ArgumentParser parser: the target argument parser.

        The method simply invokes ``ext.add_arguments(parser)`` for each
        extension ``ext`` from :attr:`.extensions`.
        """
        for key, ext in self._extensions.items():
            ext.add_arguments(parser)

    def set_defaults(self, parser):
        """Set argument defaults"""
        self.set_cmd_defaults(parser)
        self.set_ext_defaults(parser)

    def set_ext_defaults(self, parser):
        for key, ext in self._extensions.items():
            ext.set_defaults(parser)

    def add_cmd_arguments(self, parser):
        """Add command-line arguments related to this subcommand

        :param argparse.ArgumentParser parser: the target parser to be
                                               modified.

        .. note::
                A subclass shall reimplement this method to define its own
                command-line arguments. The default implementation does
                nothing.
        """
        pass

    def set_cmd_defaults(self, parser):
        pass

    def run(self):
        return 0


# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
