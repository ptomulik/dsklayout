#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import unittest.mock as mock

import dsklayout.cli.tmpdirext_ as tmpdirext_
import dsklayout.cli.ext_ as ext_


class Test__CliTmpdirExt(unittest.TestCase):

    def test__isinstance__CliExt(self):
        ext = tmpdirext_.TmpDirExt()
        self.assertIsInstance(ext, ext_.CliExt)

    def test__name(self):
        ext = tmpdirext_.TmpDirExt()
        self.assertEqual('tmpdir', ext.name)

    def test__add_arguments(self):
        ext = tmpdirext_.TmpDirExt()
        parser = mock.Mock(spec =[])
        parser.add_argument = mock.Mock()
        self.assertIsNone(ext.add_arguments(parser))
        parser.add_argument.assert_has_calls([
            mock.call("--tmpdir", dest='tmpdir', metavar='DIR', default=None, help="where to create temporary directory"),
            mock.call("--tmpdir-prefix", dest='tmpdir_prefix', metavar='PFX', default='dsklayout-', help="prefix for temporary directory name"),
        ])


if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
