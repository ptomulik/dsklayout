# -*- coding: utf8 -*-

from . import backtick_
from . import fdiskparser_
from . import misc_
import os

__all__ = ('FdiskProbe', )


class FdiskProbe(backtick_.BackTickProbe):
    """Encapsulates result of running :manpage:`fdisk(8)`.

    An instance of :class:`FdiskProbe` encapsulates a result of running

    .. code-block:: bash

        fdisk -l --bytes [DEV[ DEV[...]]]

    where ``DEV`` are block device names.
    """

    # fdisk to dsklayout field mappings: partition table metadata
    _pt_map = {
      'disklabel_type': 'label',
      'disk_identifier': 'id',
      'name': 'device',
      'units': 'units',
      'bytes': 'bytes',
    }

    # fdisk to dsklayout field mappings: partition metadata
    _pt_p_map = {
        'device': 'device',
        'start': 'start',
        'end': 'end',
        'sectors': 'size',
        'uuid': 'uuid',
        'type-uuid': 'type',
        'id': 'type',
        'name': 'name',
        'type': 'typename',
    }

    @property
    def entries(self):
        """Device names of all content entries."""
        return list(e.get('name') for e in self.content)

    @property
    def partabs(self):
        """Device names of entries having partition table."""
        return list(e.get('name') for e in self.content if 'partitions' in e)

    def entry(self, name):
        """Returns a single entry identified by device name."""
        try:
            return next((e for e in self.content if e.get('name') == name))
        except StopIteration:
            raise ValueError("invalid device name: %s" % repr(name))

    def partab(self, name):
        """Returns a dictionary which describes a partition table."""
        ent = self.entry(name)
        if 'partitions' not in ent:
            raise ValueError("entry %s has no partition table" % repr(name))
        return misc_.rekey_pt(ent, self._pt_map, self._pt_p_map)

    @classmethod
    def cmdname(cls):
        return 'fdisk'

    @classmethod
    def flags(cls, flags, **kw):
        return ['-l', '--bytes'] + flags

    @classmethod
    def kwargs(self, **kw):
        kwargs = super().kwargs(**kw)
        if 'env' not in kwargs:
            kwargs['env'] = os.environ
        kwargs['env']['LC_NUMERIC'] = 'C'  # fixes decimal point to be '.'
        return kwargs

    @classmethod
    def parse(cls, text):
        return fdiskparser_.FdiskParser().parse(text)


# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
