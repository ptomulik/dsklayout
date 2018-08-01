# -*- coding: utf8 -*-

from .. import util
import copy

__all__ = ('ArchiveMetadata',)

class ArchiveMetadata:

    __slots__ = ('_lsblk_graph', '_lvm_probe', '_mdadm_probe', '_files')

    def __init__(self, lsblk_graph=None, lvm_probe=None, mdadm_probe=None, files=None):
        self._lsblk_graph = lsblk_graph
        self._lvm_probe = lvm_probe
        self._mdadm_probe = mdadm_probe
        self._files = files or dict()

    def copy(self):
        return copy.deepcopy(self)

    @property
    def lsblk_graph(self):
        return self._lsblk_graph

    @property
    def lvm_probe(self):
        return self._lvm_probe

    @property
    def mdadm_probe(self):
        return self._mdadm_probe

    @property
    def files(self):
        return self._files

    def dump_attributes(self):
        return {'lsblk_graph': util.dump_object(self.lsblk_graph),
                'lvm_probe': util.dump_object(self.lvm_probe),
                'mdadm_probe': util.dump_object(self.mdadm_probe),
                'files': util.dump_object(self.files)}

    @classmethod
    def load_attributes(cls, attributes):
        kw = {'lsblk_graph': util.load_object(attributes['lsblk_graph']),
              'lvm_probe': util.load_object(attributes['lvm_probe']),
              'mdadm_probe': util.load_object(attributes['mdadm_probe']),
              'files': util.load_object(attributes['files'])}
        return cls(**kw)


# vim: set ft=python et ts=4 sw=4:
