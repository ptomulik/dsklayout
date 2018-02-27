#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import unittest.mock as mock

import dsklayout.cli.lsblkext_ as lsblkext_
import dsklayout.cli.cmdext_ as cmdext_
import dsklayout.info.lsblk_ as lsblk_

class Test__LsBlkExt(unittest.TestCase):

    def test__isinstance__CmdExt(self):
        ext = lsblkext_.LsBlkExt()
        self.assertIsInstance(ext, cmdext_.CmdExt)

    def test__name(self):
        self.assertEqual(lsblkext_.LsBlkExt().name, 'lsblk')

    def test__add_arguments(self):
        parser = mock.Mock(spec=[])
        parser.add_argument = mock.Mock()
        ext = lsblkext_.LsBlkExt()
        self.assertIsNone(ext.add_arguments(parser))
        parser.add_argument.assert_has_calls([
            mock.call('--lsblk', dest='lsblk', metavar='PROG', default='lsblk',
                      help='name or path to lsblk program'),
        ])

    def test__new(self):
        with mock.patch.object(lsblkext_.LsBlkExt, 'arguments') as arguments, \
             mock.patch.object(lsblk_.LsBlk, 'new', return_value ='ok') as new:
            arguments.devices = mock.Mock()
            arguments.lsblk = mock.Mock()
            ext = lsblkext_.LsBlkExt()
            self.assertEqual(ext.new(), 'ok')
            new.assert_called_once_with(arguments.devices, lsblk=arguments.lsblk)

    def test__graph(self):
        lsblk = mock.Mock()
        lsblk.graph = mock.Mock(return_value = 'ok')
        with mock.patch.object(lsblkext_.LsBlkExt, 'new', return_value = lsblk) as new:
            self.assertEqual(lsblkext_.LsBlkExt().graph(), 'ok')
            new.assert_called_once_with()

if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
