# -*- coding: utf8 -*-

from . import probe_
from . import backtick_
from . import lsblk_

__all__ = ('MdadmDetailProbe', 'MdadmExamineProbe', 'MdadmProbe')


def _select_nodes(graph, func):
    return [graph.node(n).name for n in graph.nodes if func(graph.node(n))]

class MdadmDetailProbe(backtick_.BackTickProbe):
##/dev/md2:
##
##    Version : 0.90
##     Creation Time : Wed Oct 28 21:05:20 2015
##        Raid Level : raid1
##        Array Size : 1048512 (1023.94 MiB 1073.68 MB)
##     Used Dev Size : 1048512 (1023.94 MiB 1073.68 MB)
##      Raid Devices : 2
##     Total Devices : 2
##   Preferred Minor : 2
##       Persistence : Superblock is persistent
##
##       Update Time : Thu Jul 26 14:25:15 2018
##             State : clean
##    Active Devices : 2
##   Working Devices : 2
##    Failed Devices : 0
##     Spare Devices : 0
##
##Consistency Policy : resync
##
##              UUID : b3d1b98b:dbf8bcfb:9d4deba6:47ca997f
##            Events : 0.608
##
##    Number   Major   Minor   RaidDevice State
##       0       8       18        0      active sync   /dev/sdb2
##       1       8        2        1      active sync   /dev/sda2

    @classmethod
    def command(cls, **kw):
        return kw.get('mdadm', 'mdadm')

    @classmethod
    def flags(cls, flags, **kw):
        return ['--detail'] + flags

    @classmethod
    def parse(cls, output):
        # TODO: implement parser
        return output

class MdadmExamineProbe(backtick_.BackTickProbe):
##/dev/sda2:
##          Magic : a92b4efc
##        Version : 0.90.00
##           UUID : b3d1b98b:dbf8bcfb:9d4deba6:47ca997f
##  Creation Time : Wed Oct 28 21:05:20 2015
##     Raid Level : raid1
##  Used Dev Size : 1048512 (1023.94 MiB 1073.68 MB)
##     Array Size : 1048512 (1023.94 MiB 1073.68 MB)
##   Raid Devices : 2
##  Total Devices : 2
##Preferred Minor : 2
##
##    Update Time : Thu Jul 26 14:25:15 2018
##          State : clean
## Active Devices : 2
##Working Devices : 2
## Failed Devices : 0
##  Spare Devices : 0
##       Checksum : cfa937ff - correct
##         Events : 608
##
##
##      Number   Major   Minor   RaidDevice State
##this     1       8        2        1      active sync   /dev/sda2
##
##   0     0       8       18        0      active sync   /dev/sdb2
##   1     1       8        2        1      active sync   /dev/sda2


    @classmethod
    def command(cls, **kw):
        return kw.get('mdadm', 'mdadm')

    @classmethod
    def flags(cls, flags, **kw):
        return ['--examine'] + flags

    @classmethod
    def parse(cls, output):
        # TODO: implement parser
        return output

class MdadmProbe(probe_.Probe):
    pass

# vim: set ft=python et ts=4 sw=4:
