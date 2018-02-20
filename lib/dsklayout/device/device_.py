# -*- coding: utf8 -*-
"""`dsklayout.device.device_`

Provides the Device class
"""

import abc

__all__ = ('Device',)


class Device(object, metaclass=abc.ABCMeta):
    """Represents a block device"""

    __slots__ = ()


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
