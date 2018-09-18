# -*- coding: utf8 -*-
"""Provides the CliBackupCmd class
"""

from . import cmd_
from . import progext_
from . import tmpdirext_

from ..cmd import *

__all__ = ('CliBackupCmd',)


class CliBackupCmd(cmd_.CliCmd):
    """Implements the ``dsklayout backup`` subcommand."""

    __slots__ = ()

    def __init__(self):
        super().__init__()
        progs = ('lsblk', 'fdisk', 'sfdisk', 'sgdisk', 'mdadm', 'vgcfgbackup',
                 'pvs', 'vgs', 'lvs')
        for prog in progs:
            self.add_extension(progext_.ProgExt(prog))
        self.add_extension(tmpdirext_.TmpDirExt())

    @property
    def name(self):
        return 'backup'

    @property
    def properties(self):
        """Custom properties for the ``backup`` subcommand's parser.

        .. seealso::
                :attr:`.CliCmd.properties`
        """
        return {'description': 'backup disk layout'}

    def add_cmd_arguments(self, parser):
        """Add command-line arguments related to ``backup`` subcommand.

        .. note::
                Most of the options are defined by extensions. They're handled
                separately.

        .. seealso::
                :meth:`.CliCmd.add_cmd_arguments`
        """
        parser.add_argument("outfile", metavar='OUTFILE', help="output file")
        parser.add_argument("devices", metavar='DEV', nargs='*',
                            help="block device to be included in backup")

    def run(self):
        """Execute the ``backup`` subcommand.

        .. seealso::
                :meth:`.CliCmd.run`
        """
        return BackupCmd(vars(self.arguments)).run()


# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
