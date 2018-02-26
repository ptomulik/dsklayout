# -*- coding: utf8 -*-
"""Provides the BackupAction class
"""

from . import action_
from ..util import dispatch
from ..device import *

__all__ = ('BackupAction',)


class BackupAction(action_.Action):
    """Backup action"""

    __slots__ = ('_tmpdir',)

    def __init__(self, tmpdir, **kw):
        self._tmpdir = tmpdir

    @dispatch.on('subject')
    def perform(self, subject):
        """Perform backup action on a given subject"""
        raise TypeError(("BackupAction.perform() does not accept %s as an " +
                         "argument") % type(subject).__name__)

    @dispatch.when(LinuxDevice)
    def perform(self, device):
        """Perform backup action on a linux block device"""
        return self._backup_linux_device(device)

    def _backup_linux_device(self, device):
        pass


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
