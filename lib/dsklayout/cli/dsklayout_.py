# -*- coding: utf8 -*-
"""Provides the DskLayout class
"""

from . import app_
from . import backupcmd_
from . import dotcmd_

from .. import __version__

__all__ = ('DskLayout',)


class DskLayout(app_.CliApp):

    @property
    def properties(self):
        """Properties used to create argparse.ArgumentParser"""
        return {'description': 'Retrieve and backup layouts of block devices'}

    @property
    def subcommands(self):
        return [backupcmd_.CliBackupCmd, dotcmd_.CliDotCmd]

    @property
    def version(self):
        return __version__

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
