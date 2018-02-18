# -*- coding: utf8 -*-

from . import exceptions_

import copy

__all__ = ( 'BlkDev', )

class BlkDev(object):
    """Represents a block device"""

    __slots__ = ( '_properties', '_convert' )

    # these may vary in different occurences of the device in lsblk output,
    _evolving_properties = ('pkname',)
    _converters = {
#            'name'          : str,
#            'kname'         : str,
#            'maj:min'       : str,
#            'fstype'        : str,
#            'mountpoint'    : str,
#            'label'         : str,
#            'uuid'          : str,
            'parttype'      : lambda x: int(x,16), # hex str to int
#            'partlabel'     : str,
#            'partuuid'      : str,
#            'partflags'     : str, # ? never seen...
            'ra'            : int,
            'ro'            : lambda x: bool(int(x)),
            'rm'            : lambda x: bool(int(x)),
            'hotplug'       : lambda x: bool(int(x)),
#            'model'         : str,
#            'serial'        : str,
#            'size'          : str,
#            'state'         : str,
#            'owner'         : str,
#            'group'         : str,
#            'mode'          : str,
            'alignment'     : int,
            'min-io'        : int,
            'opt-io'        : int,
            'phy-sec'       : int,
            'log-sec'       : int,
            'rota'          : lambda x: bool(int(x)),
#            'sched'         : str,
            'rq-size'       : int,
#            'type'          : str,
#            'disc-aln'      : ?, # actually it's a number with B,K,M,G.. suffix
#            'disc-gran'     : ?, # actually it's a number with B,K,M,G.. suffix
#            'disc-max'      : ?, # actually it's a number with B,K,M,G.. suffix
#            'disc-zero'     : ?, # actually it's a number with B,K,M,G.. suffix
#            'wsame'         : str,
#            'wwn'           : str,
            'rand'          : lambda x: bool(int(x)),
#            'pkname'        : str,
#            'hctl'          : str,
#            'tran'          : str,
#            'subsystems'    : str,
#            'rev'           : str,
#            'vendor'        : str
    }
    _property_map = {
            'name'          : 'name',
            'kname'         : 'kname',
            'maj_min'       : 'maj:min',
            'fstype'        : 'fstype',
            'mountpoint'    : 'mountpoint',
            'label'         : 'label',
            'uuid'          : 'uuid',
            'parttype'      : 'parttype',
            'partlabel'     : 'partlabel',
            'partuuid'      : 'partuuid',
            'partflags'     : 'partflags',
            'ra'            : 'ra',
            'ro'            : 'ro',
            'rm'            : 'rm',
            'hotplug'       : 'hotplug',
            'model'         : 'model',
            'serial'        : 'serial',
            'size'          : 'size',
            'state'         : 'state',
            'owner'         : 'owner',
            'group'         : 'group',
            'mode'          : 'mode',
            'alignment'     : 'alignment',
            'min_io'        : 'min-io',
            'opt_io'        : 'opt-io',
            'phy_sec'       : 'phy-sec',
            'log_sec'       : 'log-sec',
            'rota'          : 'rota',
            'sched'         : 'sched',
            'rq_size'       : 'rq-size',
            'type'          : 'type',
            'disc_aln'      : 'disc-aln',
            'disc_gran'     : 'disc-gran',
            'disc_max'      : 'disc-max',
            'disc_zero'     : 'disc-zero',
            'wsame'         : 'wsame',
            'wwn'           : 'wwn',
            'rand'          : 'rand',
            'pkname'        : 'pkname',
            'hctl'          : 'hctl',
            'tran'          : 'tran',
            'subsystems'    : 'subsystems',
            'rev'           : 'rev',
            'vendor'        : 'vendor',
    }

    def __init__(self, properties = (), **kw):
        self._convert = kw.get('convert', False)
        self.appear(properties)

    @property
    def properties(self):
        """The properties dictionary provided to constructor"""
        return self._properties

    @classmethod
    def convert_value(cls, key, value):
        """Convert single property value"""
        if value is not None:
            return (cls._converters.get(key, lambda x : x))(value)
        return None

    @classmethod
    def convert_values(cls, items):
        """Convert provided properties with self._converters"""
        if hasattr(items, 'items'): items = items.items()
        return { k : cls.convert_value(k,v) for k,v in items }

    def appear(self, properties):
        """Method called when node appears for the first time in lsblk output"""
        if self._convert:
            self._properties = self.convert_values(properties)
        else:
            self._properties = dict(properties)
        for k in self._evolving_properties:
            if k in properties:
                if properties[k] is None:
                    self._properties[k] = []
                else:
                    self._properties[k] = [ properties[k] ]

    def reappear(self, properties):
        """Method called when node appears again in lsblk output"""
        if self._convert:
            properties = self.convert_values(properties)
        else:
            properties = dict(properties)
        for k, v in properties.items():
            if k in self._evolving_properties:
                if k not in self._properties:
                    self._properties[k] = []
                if v is not None and v not in self._properties[k]:
                    self._properties[k].append(v)
            elif self._properties.get(k) != v:
                msg = "Conflicting values for property %s: %s vs %s" % \
                        (k, repr(self._properties.get(k)), repr(v))
                raise exceptions_.InconsistentDataError(msg)

for attr,key in BlkDev._property_map.items():
    setattr(BlkDev, attr, property(lambda self, key=key: self._properties[key]))


# vim: set ft=python et ts=4 sw=4:
