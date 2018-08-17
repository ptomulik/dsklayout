# -*- coding: utf8 -*-
"""Provides "probe" classes.

A probe object encapsulates a result of probing (querying) an operating system
for a specific information. Usually external command-line programs are used for
that. Examples of "probing" are listing disk partitions with
:manpage:`fdisk(8)` or querying raid metadata with :manpage:`mdadm(8)`.
"""

from .. import util
util.import_all_from(__package__, [
    '.probe_',
    '.backtick_',
    '.fdisk_',
    '.lsblk_',
    '.lvm_',
    '.lvs_',
    '.mdadm_',
    '.pvs_',
    '.sfdisk_',
    '.vgs_',
])

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
