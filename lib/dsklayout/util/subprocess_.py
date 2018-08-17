# -*- coding: utf8 -*-
"""Utilities for external programs' execution
"""

import subprocess

__all__ = ('backtick',)


def backtick(cmd, input=None, timeout=None, **kw):
    """Executes external command and returns its output.

    If the command exits with non-zero exit status, a ``CalledProcessError``
    exception is raised with (stdout and stderr separated).
    """
    PIPE = subprocess.PIPE
    stdin = PIPE if input is not None else None
    return subprocess.check_output(cmd, stdin=stdin, stderr=PIPE,
                                   universal_newlines=True,
                                   timeout=timeout, **kw)


# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
