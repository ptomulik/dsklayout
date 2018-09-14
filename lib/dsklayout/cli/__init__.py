# -*- coding: utf8 -*-
"""Command-line implementation.

This module implements dsklayout command-line interface. It provides an entry
point for dsklayout application -- the :func:`.main` function. The function can
be conveniently used with :func:`setuptools.setup`.

There are also classes that help implementing custom CLI applications with
subcommands and flags/options. At the top, there is :class:`.CliApp` class,
which is a base class for CLI applications (any new CLI application shall
be implemented as a subclass of :class:`CliApp`).
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

    Example usage (a code snippet for ``setup.py``)

    .. code:: python

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

__all__ = __all__ + ( 'main', )

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
