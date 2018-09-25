# -*- coding: utf8 -*-

from . import backtick_
from . import misc_
from .. import util
import json

__all__ = ('SfdiskProbe', )


class SfdiskProbe(backtick_.BackTickProbe):
    """Encapsulates result of running :manpage:`sfdisk(8)`.

    An instance of :class:`SfdiskProbe` encapsulates a result of running

    .. code-block:: bash

        sfdisk -J DEV

    where ``DEV`` is a block device name.
    """

    # sfdisk to dsklayout field mappings: partition table metadata
    _pt_map = {
        'label': 'label',
        'id': 'id',
        'device': 'device',
        'unit': 'units',
    }

    # sfdisk to dsklayout field mappings: partition metadata
    _pt_p_map = {
        'node': 'device',
        'start': 'start',
        'size': 'size',
        'uuid': 'uuid',
        'type': 'type',
        'name': 'name',
    }

    @property
    def entries(self):
        """Device names of all devices covered."""
        return [self.content['partitiontable'].get('device')]

    @property
    def partabs(self):
        """Device names of devices having partition tables."""
        return self.entries

    def entry(self, name):
        """Returns a single entry identified by device name."""
        entry = self.content['partitiontable']
        if name == entry.get('device'):
            return entry
        else:
            raise ValueError("invalid device name: %s" % repr(name))

    def partab(self, name):
        """Returns a dictionary which describes a partition table."""
        ent = self.entry(name)
        return misc_.rekey_pt(ent, self._pt_map, self._pt_p_map)

    @classmethod
    def cmdname(cls):
        return 'sfdisk'

    @classmethod
    def flags(cls, flags, **kw):
        return ['-J'] + flags

    @classmethod
    def parse(cls, text):
        return json.loads(text)

    @staticmethod
    def _compute_partition_end(part):
        try:
            start = part['start']
            size = part['size']
        except KeyError:
            pass
        else:
            part['end'] = int(start) + int(size) - 1


# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
