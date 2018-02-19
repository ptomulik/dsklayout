# -*- coding: utf8 -*-
"""`dsklayout.cli.dsklayout_`

Provides the DskLayout class
"""

from . import app_
from . import backupcmd_

__all__ = ('DskLayout',)

class DskLayout(app_.App):

    @property
    def properties(self):
        """Properties used to create argparse.ArgumentParser"""
        return { 'description': 'Retrieve and backup layouts of block devices' }

    @property
    def subcommands(self):
        return [ backupcmd_.BackupCmd ]

    def add_arguments(self, parser):
        pass

    def set_defaults(self, parser):
        pass

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
