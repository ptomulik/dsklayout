# -*- coding: utf8 -*-
"""Provides the BackupCmd class
"""

from . import cmd_
from . import lsblkext_
from . import fdiskext_
from . import sfdiskext_
from . import tmpdirext_
from ..device import *
from ..graph import *

import sys

__all__ = ('BackupCmd',)

class _PartitionTableInjector(object):

    __slots__ = ('_prober', '_candidates')

    def __init__(self, prober):
        self._prober = prober
        self._candidates = set()

    @property
    def partitioned(self):
        return self._partitioned

    @property
    def callbacks(self):
        return {'ingress_func': self.ingress_func,
                'egress_func': self.egress_func}

    def ingress_func(self, graph, node, edge):
        dev = graph.node(node)
        if dev.parttype and dev.pkname:
            self._candidates |= set(dev.pkname)

    def egress_func(self, graph, node, edge):
        if node in self._candidates:
            dev = graph.node(node)
            tab = self._prober.probe(dev.kname).partab(dev.kname)
            dev.partition_table = PartitionTable(tab)


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

    def _update_partitioned(self, graph):
        search = Dfs(direction='outward')
        updater = _PartitionTableInjector(self.sfdisk)
        search(graph, graph.roots(), **updater.callbacks)

    def _do_backup(self, tmpdir):
        graph = self.lsblk.graph(self.arguments.devices)
        # attach partition tables to nodes representing partitioned devices
        self._update_partitioned(graph)

    def run(self):
        with self.tmpdir.new() as tmpdir:
            return self._do_backup(tmpdir)
        return 0


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
