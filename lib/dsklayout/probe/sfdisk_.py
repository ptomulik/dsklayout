# -*- coding: utf8 -*-

from . import backtick_
from .. import util
from ..device import LinuxDevice
import json

__all__ = ('SfdiskProbe',)


class SfdiskProbe(backtick_.BackTickProbe):

    _device_property_map = {
        'label': 'disk-label',
        'id': 'disk-id',
    }

    @util.dispatch.on('device')
    def update_device(self, device):
        super().update_device(device)

    @util.dispatch.when(LinuxDevice)
    def update_device(self, device):
        raise NotImplementedError("Not implemented yet")

    @classmethod
    def command(cls, **kw):
        return kw.get('sfdisk', 'sfdisk')

    @classmethod
    def flags(cls, flags, **kw):
        return ['-J'] + flags

    @classmethod
    def parse(cls, output):
        return json.loads(output)


# vim: set ft=python et ts=4 sw=4:
