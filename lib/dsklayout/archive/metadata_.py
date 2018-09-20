# -*- coding: utf8 -*-

from .. import util
import copy

__all__ = ('ArchiveMetadata',)


class ArchiveMetadata:
    """Metadata for :class:`.Archive`."""

    __slots__ = ('_lsblk_graph', '_lvm_probe', '_mdadm_probe', '_files')

    def __init__(self, **kw):
        """
        :keyword .graph.Graph lsblk_graph:
            disk layout graph built by :class:`.probe.LsBlkProbe`,
        :keyword .probe.LvmProbe lvm_probe:
            a probe object with lvm probe result,
        :keyword .probe.MdadmProbe mdadm_probe: bleah 3 ...
            a probe object with mdadm probe result,
        :keyword dict files:
            a dictionary of files
        """
        self._lsblk_graph = kw.get('lsblk_graph')
        self._lvm_probe = kw.get('lvm_probe')
        self._mdadm_probe = kw.get('mdadm_probe')
        self._files = kw.get('files', dict())

    def copy(self):
        """Return a deep copy of this object.

        :rtype: ArchiveMetadata
        """
        return copy.deepcopy(self)

    @property
    def lsblk_graph(self):
        """The lsblk graph used to construct this object.

        :rtype: .graph.Graph
        """
        return self._lsblk_graph

    @property
    def lvm_probe(self):
        """The lvm probe object used to construct this object.

        :rtype: .probe.LvmProbe
        """
        return self._lvm_probe

    @property
    def mdadm_probe(self):
        """The mdadm probe object used to construct this object.

        :rtype: .probe.MdadmProbe
        """
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
