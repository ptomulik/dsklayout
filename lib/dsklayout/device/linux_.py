# -*- coding: utf8 -*-
"""Provides the LinuxDevice class
"""

from . import device_
from .. import model
from .. import util


__all__ = ('LinuxDevice',)


class LinuxDevice(device_.Device):
    """Base class for Linux block devices"""

    __slots__ = ('_properties',)

    _pp_map = dict(model.LsBlkDev._pp_map, **{
        'disk_label': 'disk-label',
        'disk_id': 'disk-id',
        'partitions': 'partitions'
    })

    def __init__(self, properties):
        self._properties = properties

    @property
    def properties(self):
        return self._properties

    def partition(self, name):
        if self.partitions is None:
            return None
        entries = [x for x in self.partitions if x.get('name') == name]
        if len(entries) != 1:
            return None
        return entries[0]

    def update_partition(self, name, properties):
        if self.partitions is None:
            self.properties['partitions'] = []
        if self.partition(name) is None:
            self.partitions.append({'name': name})
        self.partition(name).update(properties)

    @classmethod
    @util.dispatch.on('spec')
    def specargs(cls, spec):
        raise TypeError("LinuxDevice.specargs() can't take %s as argument" %
                        type(spec).__name__)

    @classmethod
    @util.dispatch.when(model.LsBlkDev)
    def specargs(cls, spec):
        return (spec.properties,)

    @classmethod
    @util.dispatch.on('spec')
    def supports(cls, spec):
        return False

    @classmethod
    @util.dispatch.when(model.LsBlkDev)
    def supports(cls, spec):
        return 1  # catch all lsblk devices not supported by others


util.add_dict_getters(LinuxDevice, LinuxDevice._pp_map, '_properties')

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
