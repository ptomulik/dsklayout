# -*- coding: utf8 -*-

from . import exceptions_

import copy

__all__ = ('BlkDev',)


class BlkDev(object):
    """Represents a block device"""

    __slots__ = ('_properties', '_convert')

    # these may vary in different occurences of the device in lsblk output,
    _evolving_properties = ('pkname',)
    _converters = {
            'parttype': lambda x: int(x, 16),  # hex str to int
            'ra': int,
            'ro': lambda x: bool(int(x)),
            'rm': lambda x: bool(int(x)),
            'hotplug': lambda x: bool(int(x)),
            'alignment': int,
            'min-io': int,
            'opt-io': int,
            'phy-sec': int,
            'log-sec': int,
            'rota': lambda x: bool(int(x)),
            'rq-size': int,
            'rand': lambda x: bool(int(x)),
    }
    _property_map = {
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

    def __init__(self, properties=(), **kw):
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
            return (cls._converters.get(key, lambda x:  x))(value)
        return None

    @classmethod
    def convert_values(cls, items):
        """Convert provided properties with self._converters"""
        if hasattr(items, 'items'):
            items = items.items()
        return {k:  cls.convert_value(k, v) for k, v in items}

    def appear(self, properties):
        """Called when node appears for the first time in lsblk output"""
        self._properties = self._convert_if_enabled(properties)
        self._for_evolving_props(self._assign_evolving_prop, properties)

    def reappear(self, properties):
        """Called when node appears again in lsblk output"""
        properties = self._convert_if_enabled(properties)

        # first verify input
        for key in (set(properties) - set(self._evolving_properties)):
            if self._properties.get(key) == properties[key]:
                continue
            msg = "Conflicting values for property %s: %s vs %s" % \
                  (key, repr(self._properties.get(key)), repr(properties[key]))
            raise exceptions_.InconsistentDataError(msg)

        # then update evolving properties
        self._for_evolving_props(self._update_evolving_prop, properties)

    def __repr__(self):
        rprops = self.__class__._repr_properties
        props = self.properties
        s = repr({k: props[k] for k in rprops if props.get(k) is not None})
        return "BlkDev(%s)" % s.replace('}', ', ...}')

    def _convert_if_enabled(self, properties):
        if self._convert:
            return self.convert_values(properties)
        else:
            return dict(properties)

    def _for_evolving_props(self, func, properties):
        for key in (set(self._evolving_properties) & set(properties)):
            func(key, properties[key])

    def _assign_evolving_prop(self, key, value):
        if value is None:
            self._properties[key] = []
        else:
            self._properties[key] = [value]

    def _update_evolving_prop(self, key, value):
        if key not in self._properties:
            self._properties[key] = []
        if value is not None and value not in self._properties[key]:
            self._properties[key].append(value)


for attr, key in BlkDev._property_map.items():
    setattr(BlkDev, attr, property(lambda self, k=key: self._properties[k]))


# vim: set ft=python et ts=4 sw=4:
