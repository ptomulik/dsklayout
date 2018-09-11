# -*- coding: utf8 -*-

from . import probe_
from .. import util
import abc

__all__ = ('BackTickProbe',)


_popen_args = ('bufsize', 'executable', 'stdin', 'stdout', 'stderr',
               'preexec_fn', 'close_fds', 'shell', 'cwd', 'env',
               'universal_newlines', 'startupinfo', 'creationflags',
               'restore_signals', 'start_new_session', 'pass_fds', 'encoding',
               'errors')


class BackTickProbe(probe_.Probe):
    """Base class for any :class:`.Probe` which retrieves content from the
    STDOUT of a *single* CLI command run.

    A subclass of :class:`.BackTickProbe` must override two methods:
    :meth:`.command` and :meth:`.parse`.

    Note, that collecting data from multiple related programs shall be
    organized differently. Inheriting :class:`.BackTickProbe` is not the
    way to go in this case.
    """

    @classmethod
    @abc.abstractmethod
    def command(cls, **kw):
        """Returns the command (path or name) used by this class.

        .. note:: This method **must** be implemented in a subclass.

        :param kw: keyword arguments (unspecified); the method receives all
                   keyword arguments passed to :meth:`.BackTickProbe.run`
                   method as is.
        :return: Path to (or name of) the CLI command that shall be used.
        :rtype: str

        :example:

        .. code-block:: python

           def command(cls, **kw):
               return kw.get('fdisk', 'fdisk')
        """
        pass

    @classmethod
    @abc.abstractmethod
    def parse(cls, output):
        """Parse output retrieved from the external program

        .. note:: This method **must** be implemented in a subclass.

        :param output: an output captured from the STDOUT of the external
                       command.
        :return: parsed data, suitable for :attr:`.content`
        :rtype: unspecified
        """
        pass

    @classmethod
    def flags(self, flags=None, **kw):
        """Returns flags that shall be passed to the external program.

        .. note:: This method **may** be customized in a subclass.

        :param flags: a list of flags as passed to :meth:`.BackTickProbe.run`;
                      ignored by the default implementation,
        :param kw:    keyword arguments as passed to
                      :meth:`.BackTickProbe.run`; ignored by the default
                      implementation.
        :type flags: list, None
        :return: A list of flags to be passed to the external command. Default
                 implementation returns an empty list ``[]`` unconditionally.
        :rtype: list
        """
        return []

    @classmethod
    def kwargs(self, **kw):
        """Returns keyword arguments to be passed to :func:`.util.backtick`

        .. note:: This method **may** be customized in a subclass

        :param kw: keyword arguments, as passed to :meth:`.BackTickProbe.run`
        :return: Keyword arguments that shall be passed to
                 :func:`.util.backtick`; the default implementation just
                 selects and returns these of **kw**, that are suitable for
                 :func:`.util.backtick`.
        :rtype: dict
        """
        return {k: v for k, v in kw.items() if k in _popen_args}

    @classmethod
    def run(cls, arguments=None, flags=None, **kw):
        """Executes an external program and returns its output as string.

        :param arguments: a list of positional arguments to be passed to the
                          external command,
        :param flags: a list of flags (options and their arguments) to be
                      passed to the external command,
        :param kw: keyword arguments; passed to :meth:`.flags` and
                   :meth:`.command`; arguments selected by :meth:`.kwargs` are
                   also passed to :func:`.util.backtick`.
        :type arguments: list, None
        :type flags: list, None
        :return: Output captured from the command (STDOUT).
        :rtype: str
        """
        if arguments is None:
            arguments = []
        elif isinstance(arguments, str):
            arguments = [arguments]
        flags = cls.flags([] if flags is None else list(flags), **kw)
        command = cls.command(**kw)
        kwargs = cls.kwargs(**kw)
        return util.backtick([command] + flags + arguments, **kwargs)

    @classmethod
    def new(cls, arguments=None, flags=None, **kw):
        """Creates a new instance for specified arguments by running the
        external command and interpreting its output.

        :param arguments: a list of positional arguments to be passed to the
                          external command; passed unchanged to
                          :meth:`.BackTickProbe.run`,
        :param flags: a list of flags (options and their arguments) to be
                      passed to the external command; passed unchanged to
                      :meth:`.BackTickProbe.run`,
        :param kw: keyword arguments; passed unchanged to
                   :meth:`.BackTickProbe.run`.
        :return: New instance of the subclass.
        """
        output = cls.run(arguments, flags, **kw)
        content = cls.parse(output)
        return cls(content)

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
