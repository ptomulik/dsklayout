#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
from unittest.mock import patch
import os.path
import json

import dsklayout.model.lsblkdev_ as lsblkdev_
import dsklayout.model.exceptions_ as exceptions_
from dsklayout.graph import *

backtick = 'dsklayout.model.lsblk_.backtick'

class Test__BlkDev(unittest.TestCase):

    def test__evolving_properties(self):
        self.assertEqual(lsblkdev_.LsBlkDev._evolving_properties, ('pkname',))

    def test__properties__1(self):
        # not officially supported, but may be stored
        blkdev = lsblkdev_.LsBlkDev({'foo':  'FOO', 'bar':  'BAR'})
        self.assertEqual(blkdev.properties, {'foo':  'FOO', 'bar':  'BAR'})

    def test__properties__2(self):
        # officially supported
        blkdev = lsblkdev_.LsBlkDev({'name': '/dev/md2', 'fstype':  'ext4'})
        self.assertEqual(blkdev.properties, {'name': '/dev/md2', 'fstype':  'ext4'})

    def test__properties__3(self):
        # officially supported
        blkdev = lsblkdev_.LsBlkDev({'name': '/dev/md2', 'pkname':  None})
        self.assertEqual(blkdev.properties, {'name': '/dev/md2', 'pkname':  []})

    def test__properties__4(self):
        # officially supported
        blkdev = lsblkdev_.LsBlkDev({'name': '/dev/md2', 'pkname':  '/dev/sda2'})
        self.assertEqual(blkdev.properties, {'name': '/dev/md2', 'pkname':  ['/dev/sda2']})

    def test__appear__1(self):
        props = {'name': '/dev/md2', 'fstype':  'ext4'}
        blkdev = lsblkdev_.LsBlkDev()
        blkdev.appear(props)
        self.assertEqual(blkdev.properties, props)
        self.assertIsNot(blkdev.properties, props) # should keep its own copy

    def test__appear__2(self):
        blkdev = lsblkdev_.LsBlkDev({'name': '/dev/md2', 'fstype':  'ext4'})
        blkdev.appear({'fstype':  'xfs', 'mountpoint':  '/home'})
        self.assertEqual(blkdev.properties, {'fstype': 'xfs', 'mountpoint': '/home'})

    def test__appear__3(self):
        blkdev = lsblkdev_.LsBlkDev({'name': '/dev/md2', 'fstype':  'ext4'})
        blkdev.appear({'fstype':  'xfs', 'pkname':  None})
        self.assertEqual(blkdev.properties, {'fstype': 'xfs', 'pkname': []})

    def test__appear__4(self):
        blkdev = lsblkdev_.LsBlkDev({'name': '/dev/md2', 'fstype':  'ext4'})
        blkdev.appear({'fstype':  'xfs', 'pkname':  '/dev/sda2'})
        self.assertEqual(blkdev.properties, {'fstype': 'xfs', 'pkname': ['/dev/sda2']})

    def test__reappear__0(self):
        props = {'name': '/dev/md2'}
        blkdev = lsblkdev_.LsBlkDev()
        with self.assertRaises(exceptions_.InconsistentDataError) as context:
            blkdev.reappear(props)
        self.assertEqual("Conflicting values for property name: %s vs %s" % (repr(None),repr('/dev/md2')), str(context.exception))

    def test__reappear__1(self):
        props = {'name': '/dev/md2', 'fstype':  'ext4', 'parttype': '0xfd'}
        blkdev = lsblkdev_.LsBlkDev(props)
        blkdev.reappear(props)
        self.assertEqual(blkdev.properties, props)
        self.assertIsNot(blkdev.properties, props) # should keep its own copy

    def test__reappear__1__convert(self):
        props = {'name': '/dev/md2', 'fstype':  'ext4', 'parttype': '0xfd'}
        blkdev = lsblkdev_.LsBlkDev(props, convert=True)
        blkdev.reappear(props)
        self.assertEqual(blkdev.properties, {'name': '/dev/md2', 'fstype': 'ext4', 'parttype': 0xfd})

    def test__reappear__2(self):
        blkdev = lsblkdev_.LsBlkDev({'name': '/dev/md2', 'fstype':  'ext4', 'mountpoint': '/home'})
        with self.assertRaises(exceptions_.InconsistentDataError) as context:
            blkdev.reappear({'name': '/dev/md2', 'fstype':  'xfs'})
        self.assertEqual("Conflicting values for property fstype: %s vs %s" % (repr('ext4'),repr('xfs')), str(context.exception))

    def test__reappear__3(self):
        blkdev = lsblkdev_.LsBlkDev({'name': '/dev/md2', 'fstype':  'ext4'})
        blkdev.reappear({'pkname': None})
        self.assertEqual(blkdev.properties, {'name': '/dev/md2', 'fstype': 'ext4', 'pkname': []})

    def test__reappear__4(self):
        blkdev = lsblkdev_.LsBlkDev({'name': '/dev/md2', 'fstype':  'ext4'})
        blkdev.reappear({'pkname': '/dev/sda2'})
        self.assertEqual(blkdev.properties, {'name': '/dev/md2', 'fstype': 'ext4', 'pkname': ['/dev/sda2']})
        blkdev.reappear({'pkname': '/dev/sdb2'})
        self.assertEqual(blkdev.properties, {'name': '/dev/md2', 'fstype': 'ext4', 'pkname': ['/dev/sda2', '/dev/sdb2']})
        blkdev.reappear({'pkname': '/dev/sda2'}) # no effect, '/dev/sda2' already in pkname
        self.assertEqual(blkdev.properties, {'name': '/dev/md2', 'fstype': 'ext4', 'pkname': ['/dev/sda2', '/dev/sdb2']})

    def test__name(self):
        blkdev = lsblkdev_.LsBlkDev({'name': '/dev/sda'})
        self.assertEqual(blkdev.name, '/dev/sda')

    def test__name__convert(self):
        blkdev = lsblkdev_.LsBlkDev({'name': '/dev/sda'}, convert=True)
        self.assertEqual(blkdev.name, '/dev/sda')

    def test__kname(self):
        blkdev = lsblkdev_.LsBlkDev({'kname': '/dev/sda'})
        self.assertEqual(blkdev.kname, '/dev/sda')

    def test__maj_min(self):
        blkdev = lsblkdev_.LsBlkDev({'maj:min': '10:20'})
        self.assertEqual(blkdev.maj_min, '10:20')

    def test__fstype(self):
        blkdev = lsblkdev_.LsBlkDev({'fstype': 'ext4'})
        self.assertEqual(blkdev.fstype, 'ext4')

    def test__mountpoint(self):
        blkdev = lsblkdev_.LsBlkDev({'mountpoint': '/home'})
        self.assertEqual(blkdev.mountpoint, '/home')

    def test__mountpoint__convert_none(self):
        blkdev = lsblkdev_.LsBlkDev({'mountpoint': None}, convert=True)
        self.assertIs(blkdev.mountpoint, None)

    def test__label(self):
        blkdev = lsblkdev_.LsBlkDev({'label': 'doom'})
        self.assertEqual(blkdev.label, 'doom')

    def test__uuid(self):
        blkdev = lsblkdev_.LsBlkDev({'uuid': 'f3681e78-b71a-437a-9268-51899002add0'})
        self.assertEqual(blkdev.uuid, 'f3681e78-b71a-437a-9268-51899002add0')

    def test__parttype(self):
        blkdev = lsblkdev_.LsBlkDev({'parttype': '0xfd'})
        self.assertEqual(blkdev.parttype, '0xfd')

    def test__parttype__convert(self):
        blkdev = lsblkdev_.LsBlkDev({'parttype': '0xfd'}, convert=True)
        self.assertIs(blkdev.parttype, 0xfd)

    def test__parttype__convert_none(self):
        blkdev = lsblkdev_.LsBlkDev({'parttype': None}, convert=True)
        self.assertIs(blkdev.parttype, None)

    def test__partlabel(self):
        blkdev = lsblkdev_.LsBlkDev({'partlabel': 'Linux RAID'})
        self.assertEqual(blkdev.partlabel, 'Linux RAID')

    def test__partuuid(self):
        blkdev = lsblkdev_.LsBlkDev({'partuuid': '5d32cd1c-1421-4cef-b33a-3430b00e86ec'})
        self.assertEqual(blkdev.partuuid, '5d32cd1c-1421-4cef-b33a-3430b00e86ec')

    def test__partflags(self):
        blkdev = lsblkdev_.LsBlkDev({'partflags': 'foo'})
        self.assertEqual(blkdev.partflags, 'foo')

    def test__ra(self):
        blkdev = lsblkdev_.LsBlkDev({'ra': '128'})
        self.assertEqual(blkdev.ra, '128')

    def test__ra__convert(self):
        blkdev = lsblkdev_.LsBlkDev({'ra': '128'}, convert=True)
        self.assertIs(blkdev.ra, 128)

    def test__ro(self):
        blkdev = lsblkdev_.LsBlkDev({'ro': '0'})
        self.assertEqual(blkdev.ro, '0')

    def test__ro__convert_false(self):
        blkdev = lsblkdev_.LsBlkDev({'ro': '0'}, convert=True)
        self.assertIs(blkdev.ro, False)

    def test__ro__convert_true(self):
        blkdev = lsblkdev_.LsBlkDev({'ro': '1'}, convert=True)
        self.assertIs(blkdev.ro, True)

    def test__rm(self):
        blkdev = lsblkdev_.LsBlkDev({'rm': '0'})
        self.assertEqual(blkdev.rm, '0')

    def test__rm__convert_false(self):
        blkdev = lsblkdev_.LsBlkDev({'rm': '0'}, convert=True)
        self.assertIs(blkdev.rm, False)

    def test__rm__convert_true(self):
        blkdev = lsblkdev_.LsBlkDev({'rm': '1'}, convert=True)
        self.assertIs(blkdev.rm, True)

    def test__hotplug(self):
        blkdev = lsblkdev_.LsBlkDev({'hotplug': '0'})
        self.assertEqual(blkdev.hotplug, '0')

    def test__hotplug__convert_false(self):
        blkdev = lsblkdev_.LsBlkDev({'hotplug': '0'}, convert=True)
        self.assertIs(blkdev.hotplug, False)

    def test__hotplug__convert_true(self):
        blkdev = lsblkdev_.LsBlkDev({'hotplug': '1'}, convert=True)
        self.assertIs(blkdev.hotplug, True)

    def test__model(self):
        blkdev = lsblkdev_.LsBlkDev({'model': 'VBOX HARDDISK'})
        self.assertEqual(blkdev.model, 'VBOX HARDDISK')

    def test__serial(self):
        blkdev = lsblkdev_.LsBlkDev({'serial': 'VBfe73cdc6-87560c44'})
        self.assertEqual(blkdev.serial, 'VBfe73cdc6-87560c44')

    def test__size(self):
        blkdev = lsblkdev_.LsBlkDev({'size': '1M'})
        self.assertEqual(blkdev.size, '1M')

    def test__state(self):
        blkdev = lsblkdev_.LsBlkDev({'state': 'running'})
        self.assertEqual(blkdev.state, 'running')

    def test__owner(self):
        blkdev = lsblkdev_.LsBlkDev({'owner': 'root'})
        self.assertEqual(blkdev.owner, 'root')

    def test__group(self):
        blkdev = lsblkdev_.LsBlkDev({'group': 'disk'})
        self.assertEqual(blkdev.group, 'disk')

    def test__mode(self):
        blkdev = lsblkdev_.LsBlkDev({'mode': 'brw-rw----'})
        self.assertEqual(blkdev.mode, 'brw-rw----')

    def test__alignment(self):
        blkdev = lsblkdev_.LsBlkDev({'alignment': '0'})
        self.assertEqual(blkdev.alignment, '0')

    def test__alignment__convert(self):
        blkdev = lsblkdev_.LsBlkDev({'alignment': '0'}, convert=True)
        self.assertIs(blkdev.alignment, 0)

    def test__min_io(self):
        blkdev = lsblkdev_.LsBlkDev({'min-io': '512'})
        self.assertEqual(blkdev.min_io, '512')

    def test__min_io__convert(self):
        blkdev = lsblkdev_.LsBlkDev({'min-io': '512'}, convert=True)
        self.assertEqual(blkdev.min_io, 512)

    def test__opt_io(self):
        blkdev = lsblkdev_.LsBlkDev({'opt-io': '0'})
        self.assertEqual(blkdev.opt_io, '0')

    def test__opt_io__convert(self):
        blkdev = lsblkdev_.LsBlkDev({'opt-io': '0'}, convert=True)
        self.assertIs(blkdev.opt_io, 0)

    def test__phy_sec(self):
        blkdev = lsblkdev_.LsBlkDev({'phy-sec': '512'})
        self.assertEqual(blkdev.phy_sec, '512')

    def test__phy_sec__convert(self):
        blkdev = lsblkdev_.LsBlkDev({'phy-sec': '512'}, convert=True)
        self.assertEqual(blkdev.phy_sec, 512)

    def test__log_sec(self):
        blkdev = lsblkdev_.LsBlkDev({'log-sec': '512'})
        self.assertEqual(blkdev.log_sec, '512')

    def test__log_sec__convert(self):
        blkdev = lsblkdev_.LsBlkDev({'log-sec': '512'}, convert=True)
        self.assertEqual(blkdev.log_sec, 512)

    def test__rota(self):
        blkdev = lsblkdev_.LsBlkDev({'rota': '1'})
        self.assertEqual(blkdev.rota, '1')

    def test__rota__convert_false(self):
        blkdev = lsblkdev_.LsBlkDev({'rota': '0'}, convert=True)
        self.assertIs(blkdev.rota, False)

    def test__rota__convert_true(self):
        blkdev = lsblkdev_.LsBlkDev({'rota': '1'}, convert=True)
        self.assertIs(blkdev.rota, True)

    def test__sched(self):
        blkdev = lsblkdev_.LsBlkDev({'sched': 'cfq'})
        self.assertEqual(blkdev.sched, 'cfq')

    def test__rq_size(self):
        blkdev = lsblkdev_.LsBlkDev({'rq-size': '128'})
        self.assertEqual(blkdev.rq_size, '128')

    def test__rq_size_convert(self):
        blkdev = lsblkdev_.LsBlkDev({'rq-size': '128'}, convert=True)
        self.assertIs(blkdev.rq_size, 128)

    def test__type(self):
        blkdev = lsblkdev_.LsBlkDev({'type': 'part'})
        self.assertEqual(blkdev.type, 'part')

    def test__disc_aln(self):
        blkdev = lsblkdev_.LsBlkDev({'disc-aln': '0'})
        self.assertEqual(blkdev.disc_aln, '0')

    def test__disc_gran(self):
        blkdev = lsblkdev_.LsBlkDev({'disc-gran': '0B'})
        self.assertEqual(blkdev.disc_gran, '0B')

    def test__disc_max(self):
        blkdev = lsblkdev_.LsBlkDev({'disc-max': '0B'})
        self.assertEqual(blkdev.disc_max, '0B')

    def test__disc_zero(self):
        blkdev = lsblkdev_.LsBlkDev({'disc-zero': '0'})
        self.assertEqual(blkdev.disc_zero, '0')

    def test__wsame(self):
        blkdev = lsblkdev_.LsBlkDev({'wsame': '0B'})
        self.assertEqual(blkdev.wsame, '0B')

    def test__wwn(self):
        blkdev = lsblkdev_.LsBlkDev({'wwn': '0x50014ee0040cf352'})
        self.assertEqual(blkdev.wwn, '0x50014ee0040cf352')

    def test__rand(self):
        blkdev = lsblkdev_.LsBlkDev({'rand': '1'})
        self.assertEqual(blkdev.rand, '1')

    def test__rand__convert_true(self):
        blkdev = lsblkdev_.LsBlkDev({'rand': '1'}, convert=True)
        self.assertIs(blkdev.rand, True)

    def test__rand__convert_false(self):
        blkdev = lsblkdev_.LsBlkDev({'rand': '0'}, convert=True)
        self.assertIs(blkdev.rand, False)

    def test__pkname(self):
        blkdev = lsblkdev_.LsBlkDev({'pkname': '/dev/sda2'})
        self.assertEqual(blkdev.pkname, ['/dev/sda2'])
        blkdev.reappear({'pkname':  '/dev/sdb2'})
        self.assertEqual(blkdev.pkname, ['/dev/sda2', '/dev/sdb2'])

    def test__hctl(self):
        blkdev = lsblkdev_.LsBlkDev({'hctl': '5:0:0:0'})
        self.assertEqual(blkdev.hctl, '5:0:0:0')

    def test__tran(self):
        blkdev = lsblkdev_.LsBlkDev({'tran': 'sata'})
        self.assertEqual(blkdev.tran, 'sata')

    def test__subsystems(self):
        blkdev = lsblkdev_.LsBlkDev({'subsystems': 'block:scsi:pci'})
        self.assertEqual(blkdev.subsystems, 'block:scsi:pci')

    def test__rev(self):
        blkdev = lsblkdev_.LsBlkDev({'rev': '1S03'})
        self.assertEqual(blkdev.rev, '1S03')

    def test__vendor(self):
        blkdev = lsblkdev_.LsBlkDev({'vendor': 'ATA'})
        self.assertEqual(blkdev.vendor, 'ATA')


if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
