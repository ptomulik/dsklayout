# -*- coding: utf8 -*-
"""Command-line implementation.

This module implements dsklayout command-line interface. The entry point for
dsklayout CLI is the :func:`.main` function, which can be conveniently used
in `setup.py`.
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
