# -*- coding: utf8 -*-
"""Dsklayout command-line implementation.

This module implements dsklayout command-line interface. It provides an entry
point for dsklayout application -- the :func:`.main` function. The function can
be conveniently used with :doc:`setuptools.setup() <setuptools>` (see the
example provided by the documentation of :func:`.main`).

There are also classes that help implementing custom CLI applications with
subcommands and flags/options. At the top, there is :class:`.CliApp` class,
which is a base class for CLI applications (any new CLI application shall
be implemented as a subclass of :class:`CliApp`). An application may implement
several subcommands. A subcommand shall be implemented as a subclass of
:class:`.CliCmd`. It may use one or more extensions. The purpose of an
extension is mainly to provide a set of specific command-line options to the
subcommand. This allows for simple re-use of options in serveral subcommands.
An extension shall be implemented as a subclass of :class:`.CliExt`.
"""

from .. import util
util.import_all_from(__package__, [
    '.app_',
    '.backupcmd_',
    '.cmd_',
    '.cmdbase_',
    '.dotcmd_',
    '.dsklayout_',
    '.ext_',
    '.progext_',
    '.tmpdirext_',
    ])


def main():
    """Entry point to the dsklayout command-line application

    :example: Usage of :func:`.main` (a code snippet for ``setup.py``)

    .. code:: python

        from setuptools import setup

        #...

        setup(name='dsklayout',
              # ... other setup arguments here ...
              entry_points={
                  'console_scripts':[
                      'dsklayout=dsklayout.cli:main'
                  ]
              }
        )
    """
    try:
        return DskLayout().run()
    except KeyboardInterrupt:
        return 0

__all__ = __all__ + ('main',)

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
