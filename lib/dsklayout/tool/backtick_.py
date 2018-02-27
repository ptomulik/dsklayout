# -*- coding: utf8 -*-

from .. import util
import abc

__all__ = ('BackTick',)


_popen_args = ('bufsize', 'executable', 'stdin', 'stdout', 'stderr',
               'preexec_fn', 'close_fds', 'shell', 'cwd', 'env',
               'universal_newlines', 'startupinfo', 'creationflags',
               'restore_signals', 'start_new_session', 'pass_fds', 'encoding',
               'errors')


class BackTick(object, metaclass=abc.ABCMeta):

    __slots__ = ('_content',)

    def __init__(self, content):
        self._content = content

    @property
    def content(self):
        return self._content

    @classmethod
    @abc.abstractmethod
    def command(self, **kw):
        """Returns the backend command used by this class"""
        pass

    @classmethod
    def flags(self, flags=None, **kw):
        """Returns flags that are passed to command"""
        return []

    @classmethod
    def kwargs(self, **kw):
        """Returns keyword arguments to be passed to backtick() function"""
        return {k: v for k, v in kw.items() if k in _popen_args}

    @classmethod
    @abc.abstractmethod
    def parse(cls, output):
        pass

    @classmethod
    def run(cls, arguments=None, flags=None, **kw):
        """Executes an external program and returns its output as string."""
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
        """Creates a new instance of BackTick for specified arguments by
           running and interpreting output of external command."""
        output = cls.run(arguments, flags, **kw)
        content = cls.parse(output)
        return cls(content)

# vim: set ft=python et ts=4 sw=4:
