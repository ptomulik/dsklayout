# -*- coding: utf8 -*-
"""Provides the BackupCmd class
"""

from . import cmd_
from . import lsblkext_
from . import fdiskext_
from . import sfdiskext_
from . import tmpdirext_
from ..device import *
##from ..graph import *
##from ..action import *

import sys

__all__ = ('BackupCmd',)


class BackupCmd(cmd_.Cmd):

    __slots__ = ()

    def __init__(self):
        super().__init__()
        self.add_extension(lsblkext_.LsBlkExt())
        self.add_extension(fdiskext_.FdiskExt())
        self.add_extension(sfdiskext_.SfdiskExt())
        self.add_extension(tmpdirext_.TmpDirExt())

    @property
    def name(self):
        return 'backup'

    @property
    def properties(self):
        return {'description': 'backup disk layout'}

    def add_cmd_arguments(self, parser):
        parser.add_argument("devices", metavar='DEV', nargs='*',
                            help="block device to be included in backup")

    def _morph_graph(self, graph):
        for devname in graph.nodes:
            graph.nodes[devname] = Device.new(graph.node(devname))

    def _backup_linux(self, tmpdir):
        graph = self.lsblk.graph(self.arguments.devices)
        # Morph LsBlkDevs into Devices
        self._morph_graph(graph)
        # 
        # TODO: finish, something like...
##            search = Dfs(direction='outward')
##            trail = search(graph, graph.roots(),
##                           ingress_func=...
##                           egress_func=...
##            action = BackupAction(tmpdir)
##            for devname in trail.nodes:
##                action(graph.node(devname))

    def run(self):
        with self.tmpdir.new() as tmpdir:
            if sys.platform == 'linux':
                return _backup_linux(tmpdir)
            else:
                raise NotImplementedError("your platform %s is not supported" 
                                          % repr(sys.platform))
        return 0


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
