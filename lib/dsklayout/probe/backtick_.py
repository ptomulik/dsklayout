# -*- coding: utf8 -*-

from . import probe_
from .. import util
import abc
import shutil

__all__ = ('BackTickProbe',)


_popen_args = ('bufsize', 'executable', 'stdin', 'stdout', 'stderr',
               'preexec_fn', 'close_fds', 'shell', 'cwd', 'env',
               'universal_newlines', 'startupinfo', 'creationflags',
               'restore_signals', 'start_new_session', 'pass_fds', 'encoding',
               'errors')


class BackTickProbe(probe_.Probe, metaclass=abc.ABCMeta):
    """Base class for any :class:`.Probe` which retrieves content from the
    STDOUT of a *single* CLI command run.

    .. note::
        Collecting data from multiple related programs shall be
        organized differently. Inheriting :class:`BackTickProbe` is not the
        proper way of implementing composite probes.

    A subclass of :class:`BackTickProbe` must override two methods:
    :meth:`command` and :meth:`parse`.

    New instances should be created by user with the class method :meth:`new`.
    A probe may be unavailable in certain circumstances. For example, a
    supporting executable may be unavailable (missing software). This is pretty
    normal (consider a host without software raid devices --
    :manpage:`mdadm(8)` is not required and most probably not installed). The
    availability of the probe may be checked with class method
    :meth:`available` before creating an instance with :meth:`new`. Trying to
    instantiate an unavailable probe will usually result with an exception.
    """

    @classmethod
    @abc.abstractmethod
    def command(cls, **kw):
        """Returns the command (path or name) used by this class.

        .. note:: This method **must** be implemented in a subclass.

        :param \*\*kw:
            keyword arguments (unspecified); the method receives all keyword
            arguments passed to :meth:`run` method as is.

        :return:
            path to (or name of) the CLI command that shall be used.
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

        :param str output:
            an output captured from the STDOUT of the external command.
        :return:
            parsed data, suitable for :attr:`.content`
        :rtype: unspecified
        """
        pass

    @classmethod
    def flags(self, flags=None, **kw):
        """Returns flags that shall be passed to the external program.

        .. note:: This method **may** be customized in a subclass.

        :param list flags:
            optional list of flags as passed to :meth:`run`; ignored by the
            default implementation,
        :param \*\*kw:
            keyword arguments, as passed to :meth:`run`; ignored by the default
            implementation.
        :return:
            a list of flags to be passed to the external command; default
            implementation returns an empty list ``[]`` unconditionally.
        :rtype: list
        """
        return []

    @classmethod
    def kwargs(self, **kw):
        """Returns keyword arguments to be passed to :func:`.util.backtick`

        .. note:: This method **may** be customized in a subclass

        :param \*\*kw:
            keyword arguments, as passed to :meth:`run`.
        :return:
            keyword arguments that shall be passed to :func:`.util.backtick`;
            the default implementation just selects and returns these of
            **kw**, that are suitable for :func:`.util.backtick`.
        :rtype: dict
        """
        return {k: v for k, v in kw.items() if k in _popen_args}

    @classmethod
    def run(cls, arguments=None, flags=None, **kw):
        """Executes an external program and returns its output as string.

        :param list arguments:
            a list of positional arguments to be passed to the external
            command,
        :param list flags:
            optional list of flags (options and their arguments) to be passed
            to the external command,
        :param \*\*kw:
            keyword arguments; passed to :meth:`flags` and :meth:`command`;
            arguments selected by :meth:`kwargs` are also passed to
            :func:`.util.backtick`.
        :return:
            output captured from the command (STDOUT).
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

        :param list arguments:
            optional list of positional arguments to be passed to the external
            command; passed unchanged to :meth:`run`,
        :param list flags:
            optional list of flags (options and their arguments) to be passed
            to the external command; passed unchanged to
            :meth:`run`,
        :param \*\*kw:
            keyword arguments; passed unchanged to :meth:`run`.
        :return:
            new instance of the subclass.
        """
        output = cls.run(arguments, flags, **kw)
        content = cls.parse(output)
        return cls(content)

    @classmethod
    def which(cls, **kw):
        """Return the path to an executable which would be run if
        :meth:`command` was called.

        :param \*\*kw:
            keyword arguments, **must** be same as keyword arguments for
            :meth:`run`.
        :return:
            the path to the supporting executable; if no command would be
            called, return ``None``.
        :rtype: str, None
        """
        return shutil.which(cls.command(**kw))

    @classmethod
    def available(cls, **kw):
        """Check if the supporting external command is available.

        :param \*\*kw:
            keyword arguments, **must** be same as keyword arguments for
            :meth:`run`.

        :return:
            ``True``, if the supporting executable is available; otherwise
            ``False``.
        """
        return bool(cls.which(kw))


# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
