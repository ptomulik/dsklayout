# -*- coding: utf8 -*-

from .. import util
import copy

__all__ = ('Device',)


class Device:
    """Represents a block device"""

    __slots__ = ('_properties', '_partition_table')

    _pp_map = {
            'name':           'name',
            'kname':          'kname',
            'maj_min':        'maj:min',
            'fstype':         'fstype',
            'mountpoint':     'mountpoint',
            'label':          'label',
            'uuid':           'uuid',
            'parttype':       'parttype',
            'partlabel':      'partlabel',
            'partuuid':       'partuuid',
            'partflags':      'partflags',
            'ra':             'ra',
            'ro':             'ro',
            'rm':             'rm',
            'hotplug':        'hotplug',
            'model':          'model',
            'serial':         'serial',
            'size':           'size',
            'state':          'state',
            'owner':          'owner',
            'group':          'group',
            'mode':           'mode',
            'alignment':      'alignment',
            'min_io':         'min-io',
            'opt_io':         'opt-io',
            'phy_sec':        'phy-sec',
            'log_sec':        'log-sec',
            'rota':           'rota',
            'sched':          'sched',
            'rq_size':        'rq-size',
            'type':           'type',
            'disc_aln':       'disc-aln',
            'disc_gran':      'disc-gran',
            'disc_max':       'disc-max',
            'disc_zero':      'disc-zero',
            'wsame':          'wsame',
            'wwn':            'wwn',
            'rand':           'rand',
            'pkname':         'pkname',
            'hctl':           'hctl',
            'tran':           'tran',
            'subsystems':     'subsystems',
            'rev':            'rev',
            'vendor':         'vendor',
    }

    _repr_properties = (
            'name',
            'kname',
            'type',
            'parttype',
            'fstype',
            'label'
    )

    def __init__(self, properties=(), partition_table=None):
        self._properties = properties
        self._partition_table = partition_table

    @property
    def properties(self):
        """The properties dictionary provided to constructor"""
        return self._properties

    @properties.setter
    def properties(self, properties):
        self._properties = properties

    @property
    def partition_table(self):
        return self._partition_table

    @partition_table.setter
    def partition_table(self, table):
        self._partition_table = table

    def __repr__(self):
        rprops = self.__class__._repr_properties
        props = self.properties
        s = repr({k: props[k] for k in rprops if props.get(k) is not None})
        return "Device(%s)" % s.replace('}', ', ...}')

    def dump_attributes(self):
        return {'properties': self.properties,
                'partition_table': util.dump_object(self.partition_table)}

    @classmethod
    def load_attributes(cls, attributes):
        partition_table = util.load_object(attributes['partition_table'])
        return cls(attributes['properties'], partition_table)


util.add_dict_getters(Device, Device._pp_map, '_properties')

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
