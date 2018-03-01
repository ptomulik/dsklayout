#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import unittest.mock as mock

import dsklayout.device.linux_ as linux_
import dsklayout.device.device_ as device_
import dsklayout.model.lsblkdev_ as lsblkdev_


class Test__LinuxDevice(unittest.TestCase):

    def test__issubclass__Device(self):
        self.assertTrue(issubclass(linux_.LinuxDevice, device_.Device))

    def test__init__1(self):
        dev = linux_.LinuxDevice('foo')
        self.assertEqual(dev.properties, 'foo')

    def test__specargs__1(self):
        with self.assertRaises(TypeError) as context:
            linux_.LinuxDevice.specargs('foo')
        self.assertEqual("LinuxDevice.specargs() can't take str as argument", str(context.exception))

    def test__specargs__2(self):
        dev = lsblkdev_.LsBlkDev({'name': '/dev/sda'})
        args = linux_.LinuxDevice.specargs(dev)
        self.assertEqual(args, (dev.properties,))

    def test__supports__1(self):
        self.assertFalse(linux_.LinuxDevice.supports('foo'))

    def test__supports__2(self):
        dev = lsblkdev_.LsBlkDev({'name': '/dev/sda'})
        self.assertEqual(linux_.LinuxDevice.supports(dev), 1)

    def test__name(self):
        dev = linux_.LinuxDevice({'name': '/dev/sda'})
        self.assertEqual(dev.name, '/dev/sda')

    def test__kname(self):
        dev = linux_.LinuxDevice({'kname': '/dev/sda'})
        self.assertEqual(dev.kname, '/dev/sda')

    def test__maj_min(self):
        dev = linux_.LinuxDevice({'maj:min': '10:20'})
        self.assertEqual(dev.maj_min, '10:20')

    def test__fstype(self):
        dev = linux_.LinuxDevice({'fstype': 'ext4'})
        self.assertEqual(dev.fstype, 'ext4')

    def test__mountpoint(self):
        dev = linux_.LinuxDevice({'mountpoint': '/home'})
        self.assertEqual(dev.mountpoint, '/home')

    def test__label(self):
        dev = linux_.LinuxDevice({'label': 'doom'})
        self.assertEqual(dev.label, 'doom')

    def test__uuid(self):
        dev = linux_.LinuxDevice({'uuid': 'f3681e78-b71a-437a-9268-51899002add0'})
        self.assertEqual(dev.uuid, 'f3681e78-b71a-437a-9268-51899002add0')

    def test__parttype(self):
        dev = linux_.LinuxDevice({'parttype': '0xfd'})
        self.assertEqual(dev.parttype, '0xfd')

    def test__partlabel(self):
        dev = linux_.LinuxDevice({'partlabel': 'Linux RAID'})
        self.assertEqual(dev.partlabel, 'Linux RAID')

    def test__partuuid(self):
        dev = linux_.LinuxDevice({'partuuid': '5d32cd1c-1421-4cef-b33a-3430b00e86ec'})
        self.assertEqual(dev.partuuid, '5d32cd1c-1421-4cef-b33a-3430b00e86ec')

    def test__partflags(self):
        dev = linux_.LinuxDevice({'partflags': 'foo'})
        self.assertEqual(dev.partflags, 'foo')

    def test__ra(self):
        dev = linux_.LinuxDevice({'ra': '128'})
        self.assertEqual(dev.ra, '128')

    def test__ro(self):
        dev = linux_.LinuxDevice({'ro': '0'})
        self.assertEqual(dev.ro, '0')

    def test__rm(self):
        dev = linux_.LinuxDevice({'rm': '0'})
        self.assertEqual(dev.rm, '0')

    def test__hotplug(self):
        dev = linux_.LinuxDevice({'hotplug': '0'})
        self.assertEqual(dev.hotplug, '0')

    def test__model(self):
        dev = linux_.LinuxDevice({'model': 'VBOX HARDDISK'})
        self.assertEqual(dev.model, 'VBOX HARDDISK')

    def test__serial(self):
        dev = linux_.LinuxDevice({'serial': 'VBfe73cdc6-87560c44'})
        self.assertEqual(dev.serial, 'VBfe73cdc6-87560c44')

    def test__size(self):
        dev = linux_.LinuxDevice({'size': '1M'})
        self.assertEqual(dev.size, '1M')

    def test__state(self):
        dev = linux_.LinuxDevice({'state': 'running'})
        self.assertEqual(dev.state, 'running')

    def test__owner(self):
        dev = linux_.LinuxDevice({'owner': 'root'})
        self.assertEqual(dev.owner, 'root')

    def test__group(self):
        dev = linux_.LinuxDevice({'group': 'disk'})
        self.assertEqual(dev.group, 'disk')

    def test__mode(self):
        dev = linux_.LinuxDevice({'mode': 'brw-rw----'})
        self.assertEqual(dev.mode, 'brw-rw----')

    def test__alignment(self):
        dev = linux_.LinuxDevice({'alignment': '0'})
        self.assertEqual(dev.alignment, '0')

    def test__min_io(self):
        dev = linux_.LinuxDevice({'min-io': '512'})
        self.assertEqual(dev.min_io, '512')

    def test__opt_io(self):
        dev = linux_.LinuxDevice({'opt-io': '0'})
        self.assertEqual(dev.opt_io, '0')

    def test__phy_sec(self):
        dev = linux_.LinuxDevice({'phy-sec': '512'})
        self.assertEqual(dev.phy_sec, '512')

    def test__log_sec(self):
        dev = linux_.LinuxDevice({'log-sec': '512'})
        self.assertEqual(dev.log_sec, '512')

    def test__rota(self):
        dev = linux_.LinuxDevice({'rota': '1'})
        self.assertEqual(dev.rota, '1')

    def test__sched(self):
        dev = linux_.LinuxDevice({'sched': 'cfq'})
        self.assertEqual(dev.sched, 'cfq')

    def test__rq_size(self):
        dev = linux_.LinuxDevice({'rq-size': '128'})
        self.assertEqual(dev.rq_size, '128')

    def test__type(self):
        dev = linux_.LinuxDevice({'type': 'part'})
        self.assertEqual(dev.type, 'part')

    def test__disc_aln(self):
        dev = linux_.LinuxDevice({'disc-aln': '0'})
        self.assertEqual(dev.disc_aln, '0')

    def test__disc_gran(self):
        dev = linux_.LinuxDevice({'disc-gran': '0B'})
        self.assertEqual(dev.disc_gran, '0B')

    def test__disc_max(self):
        dev = linux_.LinuxDevice({'disc-max': '0B'})
        self.assertEqual(dev.disc_max, '0B')

    def test__disc_zero(self):
        dev = linux_.LinuxDevice({'disc-zero': '0'})
        self.assertEqual(dev.disc_zero, '0')

    def test__wsame(self):
        dev = linux_.LinuxDevice({'wsame': '0B'})
        self.assertEqual(dev.wsame, '0B')

    def test__wwn(self):
        dev = linux_.LinuxDevice({'wwn': '0x50014ee0040cf352'})
        self.assertEqual(dev.wwn, '0x50014ee0040cf352')

    def test__rand(self):
        dev = linux_.LinuxDevice({'rand': '1'})
        self.assertEqual(dev.rand, '1')

    def test__rand(self):
        dev = linux_.LinuxDevice({'rand': True})
        self.assertIs(dev.rand, True)

    def test__pkname(self):
        dev = linux_.LinuxDevice({'pkname': ['/dev/sda2']})
        self.assertEqual(dev.pkname, ['/dev/sda2'])

    def test__hctl(self):
        dev = linux_.LinuxDevice({'hctl': '5:0:0:0'})
        self.assertEqual(dev.hctl, '5:0:0:0')

    def test__tran(self):
        dev = linux_.LinuxDevice({'tran': 'sata'})
        self.assertEqual(dev.tran, 'sata')

    def test__subsystems(self):
        dev = linux_.LinuxDevice({'subsystems': 'block:scsi:pci'})
        self.assertEqual(dev.subsystems, 'block:scsi:pci')

    def test__rev(self):
        dev = linux_.LinuxDevice({'rev': '1S03'})
        self.assertEqual(dev.rev, '1S03')

    def test__vendor(self):
        dev = linux_.LinuxDevice({'vendor': 'ATA'})
        self.assertEqual(dev.vendor, 'ATA')

    def test__disk_label(self):
        dev = linux_.LinuxDevice({'disk-label': 'dos'})
        self.assertEqual(dev.disk_label, 'dos')

    def test__disk_id(self):
        dev = linux_.LinuxDevice({'disk-id': '0x5f572a40'})
        self.assertEqual(dev.disk_id, '0x5f572a40')

if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
