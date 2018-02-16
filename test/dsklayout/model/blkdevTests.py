#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
from unittest.mock import patch
import os.path
import json

import dsklayout.model.blkdev_ as blkdev_
import dsklayout.model.exceptions_ as exceptions_
from dsklayout.graph import *

backtick = 'dsklayout.model.lsblk_.backtick'

class Test__BlkDev(unittest.TestCase):

    def test__evolving_properties(self):
        self.assertEqual(blkdev_.BlkDev._evolving_properties, ('pkname',))

    def test__properties__1(self):
        # not officially supported, but may be stored
        blkdev = blkdev_.BlkDev({'foo' : 'FOO', 'bar' : 'BAR'})
        self.assertEqual(blkdev.properties, {'foo' : 'FOO', 'bar' : 'BAR'})

    def test__properties__2(self):
        # officially supported
        blkdev = blkdev_.BlkDev({'name': '/dev/md2', 'fstype' : 'ext4'})
        self.assertEqual(blkdev.properties, {'name': '/dev/md2', 'fstype' : 'ext4'})

    def test__properties__3(self):
        # officially supported
        blkdev = blkdev_.BlkDev({'name': '/dev/md2', 'pkname' : None})
        self.assertEqual(blkdev.properties, {'name': '/dev/md2', 'pkname' : []})

    def test__properties__4(self):
        # officially supported
        blkdev = blkdev_.BlkDev({'name': '/dev/md2', 'pkname' : '/dev/sda2'})
        self.assertEqual(blkdev.properties, {'name': '/dev/md2', 'pkname' : ['/dev/sda2']})

    def test__appear__1(self):
        props = {'name': '/dev/md2', 'fstype' : 'ext4'}
        blkdev = blkdev_.BlkDev()
        blkdev.appear(props)
        self.assertEqual(blkdev.properties, props)
        self.assertIsNot(blkdev.properties, props) # should keep its own copy

    def test__appear__2(self):
        blkdev = blkdev_.BlkDev({'name': '/dev/md2', 'fstype' : 'ext4'})
        blkdev.appear({'fstype' : 'xfs', 'mountpoint' : '/home'})
        self.assertEqual(blkdev.properties, {'fstype': 'xfs', 'mountpoint': '/home'} )

    def test__appear__3(self):
        blkdev = blkdev_.BlkDev({'name': '/dev/md2', 'fstype' : 'ext4'})
        blkdev.appear({'fstype' : 'xfs', 'pkname' : None})
        self.assertEqual(blkdev.properties, {'fstype': 'xfs', 'pkname': []} )

    def test__appear__4(self):
        blkdev = blkdev_.BlkDev({'name': '/dev/md2', 'fstype' : 'ext4'})
        blkdev.appear({'fstype' : 'xfs', 'pkname' : '/dev/sda2'})
        self.assertEqual(blkdev.properties, {'fstype': 'xfs', 'pkname': ['/dev/sda2']} )

    def test__reappear__0(self):
        props = {'name': '/dev/md2'}
        blkdev = blkdev_.BlkDev()
        with self.assertRaises(exceptions_.InconsistentDataError) as context:
            blkdev.reappear(props)
        self.assertEqual("Conflicting values for property name: %s vs %s" % (repr(None),repr('/dev/md2')), str(context.exception))

    def test__reappear__1(self):
        props = {'name': '/dev/md2', 'fstype' : 'ext4', 'parttype': '0xfd'}
        blkdev = blkdev_.BlkDev(props)
        blkdev.reappear(props)
        self.assertEqual(blkdev.properties, props)
        self.assertIsNot(blkdev.properties, props) # should keep its own copy

    def test__reappear__1__convert(self):
        props = {'name': '/dev/md2', 'fstype' : 'ext4', 'parttype': '0xfd'}
        blkdev = blkdev_.BlkDev(props, convert=True)
        blkdev.reappear(props)
        self.assertEqual(blkdev.properties, {'name': '/dev/md2', 'fstype': 'ext4', 'parttype': 0xfd})

    def test__reappear__2(self):
        blkdev = blkdev_.BlkDev({'name': '/dev/md2', 'fstype' : 'ext4', 'mountpoint': '/home'})
        with self.assertRaises(exceptions_.InconsistentDataError) as context:
            blkdev.reappear({'name': '/dev/md2', 'fstype' : 'xfs'})
        self.assertEqual("Conflicting values for property fstype: %s vs %s" % (repr('ext4'),repr('xfs')), str(context.exception))

    def test__reappear__3(self):
        blkdev = blkdev_.BlkDev({'name': '/dev/md2', 'fstype' : 'ext4'})
        blkdev.reappear({'pkname': None})
        self.assertEqual(blkdev.properties, {'name': '/dev/md2', 'fstype': 'ext4', 'pkname': []})

    def test__reappear__4(self):
        blkdev = blkdev_.BlkDev({'name': '/dev/md2', 'fstype' : 'ext4'})
        blkdev.reappear({'pkname': '/dev/sda2'})
        self.assertEqual(blkdev.properties, {'name': '/dev/md2', 'fstype': 'ext4', 'pkname': ['/dev/sda2']})
        blkdev.reappear({'pkname': '/dev/sdb2'})
        self.assertEqual(blkdev.properties, {'name': '/dev/md2', 'fstype': 'ext4', 'pkname': ['/dev/sda2', '/dev/sdb2']})
        blkdev.reappear({'pkname': '/dev/sda2'}) # no effect, '/dev/sda2' already in pkname
        self.assertEqual(blkdev.properties, {'name': '/dev/md2', 'fstype': 'ext4', 'pkname': ['/dev/sda2', '/dev/sdb2']})

    def test__name(self):
        blkdev = blkdev_.BlkDev({'name': '/dev/sda'})
        self.assertEqual(blkdev.name, '/dev/sda')

    def test__name__convert(self):
        blkdev = blkdev_.BlkDev({'name': '/dev/sda'}, convert=True)
        self.assertEqual(blkdev.name, '/dev/sda')

    def test__kname(self):
        blkdev = blkdev_.BlkDev({'kname': '/dev/sda'})
        self.assertEqual(blkdev.kname, '/dev/sda')

    def test__maj_min(self):
        blkdev = blkdev_.BlkDev({'maj:min': '10:20'})
        self.assertEqual(blkdev.maj_min, '10:20')

    def test__fstype(self):
        blkdev = blkdev_.BlkDev({'fstype': 'ext4'})
        self.assertEqual(blkdev.fstype, 'ext4')

    def test__mountpoint(self):
        blkdev = blkdev_.BlkDev({'mountpoint': '/home'})
        self.assertEqual(blkdev.mountpoint, '/home')

    def test__mountpoint__convert_none(self):
        blkdev = blkdev_.BlkDev({'mountpoint': None}, convert=True)
        self.assertIs(blkdev.mountpoint, None)

    def test__label(self):
        blkdev = blkdev_.BlkDev({'label': 'doom'})
        self.assertEqual(blkdev.label, 'doom')

    def test__uuid(self):
        blkdev = blkdev_.BlkDev({'uuid': 'f3681e78-b71a-437a-9268-51899002add0'})
        self.assertEqual(blkdev.uuid, 'f3681e78-b71a-437a-9268-51899002add0')

    def test__parttype(self):
        blkdev = blkdev_.BlkDev({'parttype': '0xfd'})
        self.assertEqual(blkdev.parttype, '0xfd')

    def test__parttype__convert(self):
        blkdev = blkdev_.BlkDev({'parttype': '0xfd'}, convert=True)
        self.assertIs(blkdev.parttype, 0xfd)

    def test__parttype__convert_none(self):
        blkdev = blkdev_.BlkDev({'parttype': None}, convert=True)
        self.assertIs(blkdev.parttype, None)

    def test__partlabel(self):
        blkdev = blkdev_.BlkDev({'partlabel': 'Linux RAID'})
        self.assertEqual(blkdev.partlabel, 'Linux RAID')

    def test__partuuid(self):
        blkdev = blkdev_.BlkDev({'partuuid': '5d32cd1c-1421-4cef-b33a-3430b00e86ec'})
        self.assertEqual(blkdev.partuuid, '5d32cd1c-1421-4cef-b33a-3430b00e86ec')

    def test__partflags(self):
        blkdev = blkdev_.BlkDev({'partflags': 'foo'})
        self.assertEqual(blkdev.partflags, 'foo')

    def test__ra(self):
        blkdev = blkdev_.BlkDev({'ra': '128'})
        self.assertEqual(blkdev.ra, '128')

    def test__ra__convert(self):
        blkdev = blkdev_.BlkDev({'ra': '128'}, convert=True)
        self.assertIs(blkdev.ra, 128)

    def test__ro(self):
        blkdev = blkdev_.BlkDev({'ro': '0'})
        self.assertEqual(blkdev.ro, '0')

    def test__ro__convert_false(self):
        blkdev = blkdev_.BlkDev({'ro': '0'}, convert=True)
        self.assertIs(blkdev.ro, False)

    def test__ro__convert_true(self):
        blkdev = blkdev_.BlkDev({'ro': '1'}, convert=True)
        self.assertIs(blkdev.ro, True)

    def test__rm(self):
        blkdev = blkdev_.BlkDev({'rm': '0'})
        self.assertEqual(blkdev.rm, '0')

    def test__rm__convert_false(self):
        blkdev = blkdev_.BlkDev({'rm': '0'}, convert=True)
        self.assertIs(blkdev.rm, False)

    def test__rm__convert_true(self):
        blkdev = blkdev_.BlkDev({'rm': '1'}, convert=True)
        self.assertIs(blkdev.rm, True)

    def test__hotplug(self):
        blkdev = blkdev_.BlkDev({'hotplug': '0'})
        self.assertEqual(blkdev.hotplug, '0')

    def test__hotplug__convert_false(self):
        blkdev = blkdev_.BlkDev({'hotplug': '0'}, convert=True)
        self.assertIs(blkdev.hotplug, False)

    def test__hotplug__convert_true(self):
        blkdev = blkdev_.BlkDev({'hotplug': '1'}, convert=True)
        self.assertIs(blkdev.hotplug, True)

    def test__model(self):
        blkdev = blkdev_.BlkDev({'model': 'VBOX HARDDISK'})
        self.assertEqual(blkdev.model, 'VBOX HARDDISK')

    def test__serial(self):
        blkdev = blkdev_.BlkDev({'serial': 'VBfe73cdc6-87560c44'})
        self.assertEqual(blkdev.serial, 'VBfe73cdc6-87560c44')

    def test__size(self):
        blkdev = blkdev_.BlkDev({'size': '1M'})
        self.assertEqual(blkdev.size, '1M')

    def test__state(self):
        blkdev = blkdev_.BlkDev({'state': 'running'})
        self.assertEqual(blkdev.state, 'running')

    def test__owner(self):
        blkdev = blkdev_.BlkDev({'owner': 'root'})
        self.assertEqual(blkdev.owner, 'root')

    def test__group(self):
        blkdev = blkdev_.BlkDev({'group': 'disk'})
        self.assertEqual(blkdev.group, 'disk')

    def test__mode(self):
        blkdev = blkdev_.BlkDev({'mode': 'brw-rw----'})
        self.assertEqual(blkdev.mode, 'brw-rw----')

    def test__alignment(self):
        blkdev = blkdev_.BlkDev({'alignment': '0'})
        self.assertEqual(blkdev.alignment, '0')

    def test__alignment__convert(self):
        blkdev = blkdev_.BlkDev({'alignment': '0'}, convert=True)
        self.assertIs(blkdev.alignment, 0)

    def test__min_io(self):
        blkdev = blkdev_.BlkDev({'min-io': '512'})
        self.assertEqual(blkdev.min_io, '512')

    def test__min_io__convert(self):
        blkdev = blkdev_.BlkDev({'min-io': '512'}, convert=True)
        self.assertEqual(blkdev.min_io, 512)

    def test__opt_io(self):
        blkdev = blkdev_.BlkDev({'opt-io': '0'})
        self.assertEqual(blkdev.opt_io, '0')

    def test__opt_io__convert(self):
        blkdev = blkdev_.BlkDev({'opt-io': '0'}, convert=True)
        self.assertIs(blkdev.opt_io, 0)

    def test__phy_sec(self):
        blkdev = blkdev_.BlkDev({'phy-sec': '512'})
        self.assertEqual(blkdev.phy_sec, '512')

    def test__phy_sec__convert(self):
        blkdev = blkdev_.BlkDev({'phy-sec': '512'}, convert=True)
        self.assertEqual(blkdev.phy_sec, 512)

    def test__log_sec(self):
        blkdev = blkdev_.BlkDev({'log-sec': '512'})
        self.assertEqual(blkdev.log_sec, '512')

    def test__log_sec__convert(self):
        blkdev = blkdev_.BlkDev({'log-sec': '512'}, convert=True)
        self.assertEqual(blkdev.log_sec, 512)

    def test__rota(self):
        blkdev = blkdev_.BlkDev({'rota': '1'})
        self.assertEqual(blkdev.rota, '1')

    def test__rota__convert_false(self):
        blkdev = blkdev_.BlkDev({'rota': '0'}, convert=True)
        self.assertIs(blkdev.rota, False)

    def test__rota__convert_true(self):
        blkdev = blkdev_.BlkDev({'rota': '1'}, convert=True)
        self.assertIs(blkdev.rota, True)

    def test__sched(self):
        blkdev = blkdev_.BlkDev({'sched': 'cfq'})
        self.assertEqual(blkdev.sched, 'cfq')

    def test__rq_size(self):
        blkdev = blkdev_.BlkDev({'rq-size': '128'})
        self.assertEqual(blkdev.rq_size, '128')

    def test__rq_size_convert(self):
        blkdev = blkdev_.BlkDev({'rq-size': '128'}, convert=True)
        self.assertIs(blkdev.rq_size, 128)

    def test__type(self):
        blkdev = blkdev_.BlkDev({'type': 'part'})
        self.assertEqual(blkdev.type, 'part')

    def test__disc_aln(self):
        blkdev = blkdev_.BlkDev({'disc-aln': '0'})
        self.assertEqual(blkdev.disc_aln, '0')

    def test__disc_gran(self):
        blkdev = blkdev_.BlkDev({'disc-gran': '0B'})
        self.assertEqual(blkdev.disc_gran, '0B')

    def test__disc_max(self):
        blkdev = blkdev_.BlkDev({'disc-max': '0B'})
        self.assertEqual(blkdev.disc_max, '0B')

    def test__disc_zero(self):
        blkdev = blkdev_.BlkDev({'disc-zero': '0'})
        self.assertEqual(blkdev.disc_zero, '0')

    def test__wsame(self):
        blkdev = blkdev_.BlkDev({'wsame': '0B'})
        self.assertEqual(blkdev.wsame, '0B')

    def test__wwn(self):
        blkdev = blkdev_.BlkDev({'wwn': '0x50014ee0040cf352'})
        self.assertEqual(blkdev.wwn, '0x50014ee0040cf352')

    def test__rand(self):
        blkdev = blkdev_.BlkDev({'rand': '1'})
        self.assertEqual(blkdev.rand, '1')

    def test__rand__convert_true(self):
        blkdev = blkdev_.BlkDev({'rand': '1'}, convert=True)
        self.assertIs(blkdev.rand, True)

    def test__rand__convert_false(self):
        blkdev = blkdev_.BlkDev({'rand': '0'}, convert=True)
        self.assertIs(blkdev.rand, False)

    def test__pkname(self):
        blkdev = blkdev_.BlkDev({'pkname': '/dev/sda2'})
        self.assertEqual(blkdev.pkname, ['/dev/sda2'])
        blkdev.reappear({'pkname' : '/dev/sdb2'})
        self.assertEqual(blkdev.pkname, ['/dev/sda2', '/dev/sdb2'])

    def test__hctl(self):
        blkdev = blkdev_.BlkDev({'hctl': '5:0:0:0'})
        self.assertEqual(blkdev.hctl, '5:0:0:0')

    def test__tran(self):
        blkdev = blkdev_.BlkDev({'tran': 'sata'})
        self.assertEqual(blkdev.tran, 'sata')

    def test__subsystems(self):
        blkdev = blkdev_.BlkDev({'subsystems': 'block:scsi:pci'})
        self.assertEqual(blkdev.subsystems, 'block:scsi:pci')

    def test__rev(self):
        blkdev = blkdev_.BlkDev({'rev': '1S03'})
        self.assertEqual(blkdev.rev, '1S03')

    def test__vendor(self):
        blkdev = blkdev_.BlkDev({'vendor': 'ATA'})
        self.assertEqual(blkdev.vendor, 'ATA')


if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
