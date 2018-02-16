# -*- coding: utf8 -*-

from . import exceptions_

__all__ = ( 'BlkDev', )

class BlkDev(object):
    """Represents a block device"""

    __slots__ = ( '_properties', '_convert' )

    # these may vary in different occurences of the device in lsblk output,
    _evolving_properties = ('pkname',)
    _converters = {
#            'name'          : str,
#            'kname'         : str,
#            'maj-min'       : str,
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

    @property
    def name(self):
        """Device name"""
        return self._properties['name']

    @property
    def kname(self):
        """Internal kernel device name"""
        return self._properties['kname']

    @property
    def maj_min(self):
        """Major:minor device number"""
        return self._properties['maj:min']

    @property
    def fstype(self):
        """Filesystem type"""
        return self._properties['fstype']

    @property
    def mountpoint(self):
        """Where the device is mounted"""
        return self._properties['mountpoint']

    @property
    def label(self):
        """Filesystem LABEL"""
        return self._properties['label']

    @property
    def uuid(self):
        """Filesystem UUID"""
        return self._properties['uuid']

    @property
    def parttype(self):
        """Partition type UUID"""
        return self._properties['parttype']

    @property
    def partlabel(self):
        """Partition LABEL"""
        return self._properties['partlabel']

    @property
    def partuuid(self):
        """Partition UUID"""
        return self._properties['partuuid']

    @property
    def partflags(self):
        """Partition flags"""
        return self._properties['partflags']

    @property
    def ra(self):
        """Read-ahead of the device"""
        return self._properties['ra']

    @property
    def ro(self):
        """Read-only device"""
        return self._properties['ro']

    @property
    def rm(self):
        """Removable device"""
        return self._properties['rm']

    @property
    def hotplug(self):
        """Removable or hotplug device (usb, pcmcia, ...)"""
        return self._properties['hotplug']

    @property
    def model(self):
        """Device identifier"""
        return self._properties['model']

    @property
    def serial(self):
        """Disk serial number"""
        return self._properties['serial']

    @property
    def size(self):
        """Size of the device"""
        return self._properties['size']

    @property
    def state(self):
        """State of the device"""
        return self._properties['state']

    @property
    def owner(self):
        """User name"""
        return self._properties['owner']

    @property
    def group(self):
        """Group name"""
        return self._properties['group']

    @property
    def mode(self):
        """Device node permissions"""
        return self._properties['mode']

    @property
    def alignment(self):
        """Alignment offset"""
        return self._properties['alignment']

    @property
    def min_io(self):
        """Minimum I/O size"""
        return self._properties['min-io']

    @property
    def opt_io(self):
        """Optimal I/O size"""
        return self._properties['opt-io']

    @property
    def phy_sec(self):
        """Physical sector size"""
        return self._properties['phy-sec']

    @property
    def log_sec(self):
        """Logical sector size"""
        return self._properties['log-sec']

    @property
    def rota(self):
        """Rotational device"""
        return self._properties['rota']

    @property
    def sched(self):
        """I/O scheduler name"""
        return self._properties['sched']

    @property
    def rq_size(self):
        """Request queue size"""
        return self._properties['rq-size']

    @property
    def type(self):
        """Device type"""
        return self._properties['type']

    @property
    def disc_aln(self):
        """Discard alignment offset"""
        return self._properties['disc-aln']

    @property
    def disc_gran(self):
        """Discard granularity"""
        return self._properties['disc-gran']

    @property
    def disc_max(self):
        """Discard max bytes"""
        return self._properties['disc-max']

    @property
    def disc_zero(self):
        """Discard zeroes data"""
        return self._properties['disc-zero']

    @property
    def wsame(self):
        """Write same max bytes"""
        return self._properties['wsame']

    @property
    def wwn(self):
        """Unique storage identifier"""
        return self._properties['wwn']

    @property
    def rand(self):
        """Adds randomness"""
        return self._properties['rand']

    @property
    def pkname(self):
        """Internal parent kernel device name"""
        return self._properties['pkname']

    @property
    def hctl(self):
        """Host:Channel:Target:Lun for SCSI"""
        return self._properties['hctl']

    @property
    def tran(self):
        """Device transport type"""
        return self._properties['tran']

    @property
    def subsystems(self):
        """De-duplicated chain of subsystems"""
        return self._properties['subsystems']

    @property
    def rev(self):
        """Device revision"""
        return self._properties['rev']

    @property
    def vendor(self):
        """Device vendor"""
        return self._properties['vendor']



# vim: set ft=python et ts=4 sw=4:
