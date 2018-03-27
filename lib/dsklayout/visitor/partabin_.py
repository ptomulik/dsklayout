# -*- coding: utf8 -*-
"""Provides the ParTabIn class
"""

from .. import device

__all__ = ('ParTabIn',)


class ParTabIn:
    """Partition Table Injector"""

    __slots__ = ('_candidates', '_prober')

    def __init__(self, prober):
        """Initializes the injector."""
        self._prober = prober
        self._candidates = set()

    @property
    def callbacks(self):
        return {'ingress_func': self.ingress, 'egress_func': self.egress}

    @property
    def prober(self):
        return self._prober

    def ingress(self, graph, node, edge):
        dev = graph.node(node)
        if dev.parttype and dev.pkname:
            self._candidates |= set(dev.pkname)

    def egress(self, graph, node, edge):
        if node in self._candidates:
            dev = graph.node(node)
            tab = self.prober(node)
            if tab:
                dev.partition_table = device.PartitionTable.new(tab)


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
