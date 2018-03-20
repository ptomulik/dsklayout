#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
from unittest.mock import patch
import os.path
import json

import dsklayout.device.device_ as device_
from dsklayout.graph import *

class Test__Device(unittest.TestCase):

    def test__properties__1(self):
        # not officially supported, but may be stored
        dev = device_.Device({'foo':  'FOO', 'bar':  'BAR'})
        self.assertEqual(dev.properties, {'foo':  'FOO', 'bar':  'BAR'})

    def test__properties__2(self):
        # officially supported
        dev = device_.Device({'name': '/dev/md2', 'fstype':  'ext4'})
        self.assertEqual(dev.properties, {'name': '/dev/md2', 'fstype':  'ext4'})

    def test__properties__3(self):
        # officially supported
        dev = device_.Device({'name': '/dev/md2', 'pkname':  None})
        self.assertEqual(dev.properties, {'name': '/dev/md2', 'pkname':  None})

    def test__properties__4(self):
        # officially supported
        dev = device_.Device({'name': '/dev/md2', 'pkname':  '/dev/sda2'})
        self.assertEqual(dev.properties, {'name': '/dev/md2', 'pkname':  '/dev/sda2'})

    def test__partition_table__1(self):
        dev = device_.Device()
        self.assertIsNone(dev.partition_table)

    def test__partition_table__2(self):
        dev = device_.Device((), 'foo')
        self.assertEqual(dev.partition_table, 'foo')

    def test__partition_table__3(self):
        dev = device_.Device((), 'foo')
        dev.partition_table = 'bar'
        self.assertEqual(dev.partition_table, 'bar')

    def test__repr__(self):
        dev = device_.Device({'name': '/dev/foo/bar', 'kname': '/dev/dm0',
                                     'type': 'disk', 'parttype': None, 'fstype':  'ext4',
                                     'label': 'Penguin'})
        s = repr(dev)
        self.assertIn('Device(', s)
        self.assertIn('...}', s)
        self.assertIn('name', s)
        self.assertIn('/dev/foo/bar', s)
        self.assertIn('kname', s)
        self.assertIn('/dev/dm0', s)
        self.assertIn('type', s)
        self.assertIn('disk', s)
        self.assertNotIn('parttype', s)
        self.assertNotIn('None', s)
        self.assertIn('fstype', s)
        self.assertIn('ext4', s)
        self.assertIn('label', s)
        self.assertIn('Penguin', s)

    def test__name(self):
        dev = device_.Device({'name': '/dev/sda'})
        self.assertEqual(dev.name, '/dev/sda')

    def test__kname(self):
        dev = device_.Device({'kname': '/dev/sda'})
        self.assertEqual(dev.kname, '/dev/sda')

    def test__maj_min(self):
        dev = device_.Device({'maj:min': '10:20'})
        self.assertEqual(dev.maj_min, '10:20')

    def test__fstype(self):
        dev = device_.Device({'fstype': 'ext4'})
        self.assertEqual(dev.fstype, 'ext4')

    def test__mountpoint(self):
        dev = device_.Device({'mountpoint': '/home'})
        self.assertEqual(dev.mountpoint, '/home')

    def test__label(self):
        dev = device_.Device({'label': 'doom'})
        self.assertEqual(dev.label, 'doom')

    def test__uuid(self):
        dev = device_.Device({'uuid': 'f3681e78-b71a-437a-9268-51899002add0'})
        self.assertEqual(dev.uuid, 'f3681e78-b71a-437a-9268-51899002add0')

    def test__parttype(self):
        dev = device_.Device({'parttype': '0xfd'})
        self.assertEqual(dev.parttype, '0xfd')

    def test__partlabel(self):
        dev = device_.Device({'partlabel': 'Linux RAID'})
        self.assertEqual(dev.partlabel, 'Linux RAID')

    def test__partuuid(self):
        dev = device_.Device({'partuuid': '5d32cd1c-1421-4cef-b33a-3430b00e86ec'})
        self.assertEqual(dev.partuuid, '5d32cd1c-1421-4cef-b33a-3430b00e86ec')

    def test__partflags(self):
        dev = device_.Device({'partflags': 'foo'})
        self.assertEqual(dev.partflags, 'foo')

    def test__ra(self):
        dev = device_.Device({'ra': '128'})
        self.assertEqual(dev.ra, '128')

    def test__ro(self):
        dev = device_.Device({'ro': '0'})
        self.assertEqual(dev.ro, '0')

    def test__rm(self):
        dev = device_.Device({'rm': '0'})
        self.assertEqual(dev.rm, '0')

    def test__hotplug(self):
        dev = device_.Device({'hotplug': '0'})
        self.assertEqual(dev.hotplug, '0')

    def test__model(self):
        dev = device_.Device({'model': 'VBOX HARDDISK'})
        self.assertEqual(dev.model, 'VBOX HARDDISK')

    def test__serial(self):
        dev = device_.Device({'serial': 'VBfe73cdc6-87560c44'})
        self.assertEqual(dev.serial, 'VBfe73cdc6-87560c44')

    def test__size(self):
        dev = device_.Device({'size': '1M'})
        self.assertEqual(dev.size, '1M')

    def test__state(self):
        dev = device_.Device({'state': 'running'})
        self.assertEqual(dev.state, 'running')

    def test__owner(self):
        dev = device_.Device({'owner': 'root'})
        self.assertEqual(dev.owner, 'root')

    def test__group(self):
        dev = device_.Device({'group': 'disk'})
        self.assertEqual(dev.group, 'disk')

    def test__mode(self):
        dev = device_.Device({'mode': 'brw-rw----'})
        self.assertEqual(dev.mode, 'brw-rw----')

    def test__alignment(self):
        dev = device_.Device({'alignment': '0'})
        self.assertEqual(dev.alignment, '0')

    def test__min_io(self):
        dev = device_.Device({'min-io': '512'})
        self.assertEqual(dev.min_io, '512')

    def test__opt_io(self):
        dev = device_.Device({'opt-io': '0'})
        self.assertEqual(dev.opt_io, '0')

    def test__phy_sec(self):
        dev = device_.Device({'phy-sec': '512'})
        self.assertEqual(dev.phy_sec, '512')

    def test__log_sec(self):
        dev = device_.Device({'log-sec': '512'})
        self.assertEqual(dev.log_sec, '512')

    def test__rota(self):
        dev = device_.Device({'rota': '1'})
        self.assertEqual(dev.rota, '1')

    def test__sched(self):
        dev = device_.Device({'sched': 'cfq'})
        self.assertEqual(dev.sched, 'cfq')

    def test__rq_size(self):
        dev = device_.Device({'rq-size': '128'})
        self.assertEqual(dev.rq_size, '128')

    def test__type(self):
        dev = device_.Device({'type': 'part'})
        self.assertEqual(dev.type, 'part')

    def test__disc_aln(self):
        dev = device_.Device({'disc-aln': '0'})
        self.assertEqual(dev.disc_aln, '0')

    def test__disc_gran(self):
        dev = device_.Device({'disc-gran': '0B'})
        self.assertEqual(dev.disc_gran, '0B')

    def test__disc_max(self):
        dev = device_.Device({'disc-max': '0B'})
        self.assertEqual(dev.disc_max, '0B')

    def test__disc_zero(self):
        dev = device_.Device({'disc-zero': '0'})
        self.assertEqual(dev.disc_zero, '0')

    def test__wsame(self):
        dev = device_.Device({'wsame': '0B'})
        self.assertEqual(dev.wsame, '0B')

    def test__wwn(self):
        dev = device_.Device({'wwn': '0x50014ee0040cf352'})
        self.assertEqual(dev.wwn, '0x50014ee0040cf352')

    def test__rand(self):
        dev = device_.Device({'rand': '1'})
        self.assertEqual(dev.rand, '1')

    def test__pkname(self):
        dev = device_.Device({'pkname': '/dev/sda2'})
        self.assertEqual(dev.pkname, '/dev/sda2')

    def test__hctl(self):
        dev = device_.Device({'hctl': '5:0:0:0'})
        self.assertEqual(dev.hctl, '5:0:0:0')

    def test__tran(self):
        dev = device_.Device({'tran': 'sata'})
        self.assertEqual(dev.tran, 'sata')

    def test__subsystems(self):
        dev = device_.Device({'subsystems': 'block:scsi:pci'})
        self.assertEqual(dev.subsystems, 'block:scsi:pci')

    def test__rev(self):
        dev = device_.Device({'rev': '1S03'})
        self.assertEqual(dev.rev, '1S03')

    def test__vendor(self):
        dev = device_.Device({'vendor': 'ATA'})
        self.assertEqual(dev.vendor, 'ATA')


if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
