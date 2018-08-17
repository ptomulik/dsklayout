# -*- coding: utf8 -*-

from .. import util
import copy

__all__ = ('ArchiveMetadata',)


class ArchiveMetadata:

    __slots__ = ('_lsblk_graph', '_lvm_probe', '_mdadm_probe', '_files')

    def __init__(self, **kw):
        self._lsblk_graph = kw.get('lsblk_graph')
        self._lvm_probe = kw.get('lvm_probe')
        self._mdadm_probe = kw.get('mdadm_probe')
        self._files = kw.get('files', dict())

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


# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
