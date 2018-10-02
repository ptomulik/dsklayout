#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import unittest.mock as mock
from unittest.mock import patch

import dsklayout.archive.metadata_ as metadata_

class Test__ArchiveMetadata(unittest.TestCase):

    def test__init__0(self):
        meta = metadata_.ArchiveMetadata()
        self.assertIsNone(meta._lsblk_graph)
        self.assertEqual(meta._files, dict())

    def test__init__1(self):
        graph = mock.Mock(spec=True)
        meta = metadata_.ArchiveMetadata(lsblk_graph=graph)
        self.assertIs(meta._lsblk_graph, graph)

    def test__init__2(self):
        lvm = mock.Mock(spec=True)
        meta = metadata_.ArchiveMetadata(lvm_probe=lvm)
        self.assertIs(meta._lvm_probe, lvm)

    def test__init__3(self):
        mdadm = mock.Mock(spec=True)
        meta = metadata_.ArchiveMetadata(mdadm_probe=mdadm)
        self.assertIs(meta._mdadm_probe, mdadm)

    def test__lsblk_graph__1(self):
        meta = metadata_.ArchiveMetadata()
        self.assertIsNone(meta.lsblk_graph)
        meta._lsblk_graph = mock.Mock(spec=True)
        self.assertIs(meta.lsblk_graph, meta._lsblk_graph)

    def test__lvm_probe__1(self):
        meta = metadata_.ArchiveMetadata()
        self.assertIsNone(meta.lvm_probe)
        meta._lvm_probe = mock.Mock(spec=True)
        self.assertIs(meta.lvm_probe, meta._lvm_probe)

    def test__mdadm_probe__1(self):
        meta = metadata_.ArchiveMetadata()
        self.assertIsNone(meta.mdadm_probe)
        meta._mdadm_probe = mock.Mock(spec=True)
        self.assertIs(meta.mdadm_probe, meta._mdadm_probe)

    def test__files__1(self):
        meta = metadata_.ArchiveMetadata()
        self.assertEqual(meta.files, dict())
        meta._files = mock.Mock(spec=True)
        self.assertIs(meta.files, meta._files)

    def test__copy(self):
        meta = metadata_.ArchiveMetadata()
        with patch('copy.deepcopy', return_value='ok') as deepcopy:
            self.assertEqual(meta.copy(), 'ok')
            deepcopy.assert_called_once_with(meta)

    def test__dump_attributes(self):
        graph = mock.Mock(spec=True, foo='graph!')
        lvm = mock.Mock(spec=True, foo='lvm!')
        mdadm = mock.Mock(spec=True, foo='mdadm!')
        files = mock.Mock(spec=True, foo='files!')
        meta = metadata_.ArchiveMetadata(lsblk_graph=graph, lvm_probe=lvm, mdadm_probe=mdadm, files=files)
        with patch('dsklayout.util.dump_object', side_effect=lambda x: x.foo) as dump_object:
            self.assertEqual(meta.dump_attributes(), {'lsblk_graph': 'graph!', 'lvm_probe': 'lvm!', 'mdadm_probe': 'mdadm!', 'files': 'files!'})
            dump_object.assert_has_calls([mock.call(graph), mock.call(lvm), mock.call(mdadm), mock.call(files)])

    def test__load_attributes(self):
        graph = mock.Mock(spec=True, foo='graph!')
        lvm = mock.Mock(spec=True, foo='lvm!')
        mdadm = mock.Mock(spec=True, foo='mdadm!')
        files = mock.Mock(spec=True, foo='files!')
        attributes = {'lsblk_graph': graph,
                      'lvm_probe': lvm,
                      'mdadm_probe': mdadm,
                      'files': files }
        with patch('dsklayout.util.load_object', side_effect=lambda x: x.foo) as load_object:
            meta = metadata_.ArchiveMetadata.load_attributes(attributes)
            self.assertIsInstance(meta, metadata_.ArchiveMetadata)
            self.assertEqual(meta.lsblk_graph, 'graph!')
            self.assertEqual(meta.lvm_probe, 'lvm!')
            self.assertEqual(meta.mdadm_probe, 'mdadm!')
            self.assertEqual(meta.files, 'files!')
            load_object.assert_has_calls([mock.call(graph), mock.call(lvm), mock.call(mdadm), mock.call(files)])


if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
