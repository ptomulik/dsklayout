#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import dsklayout.archive as archive


class Test__archive__PackageSymbols(unittest.TestCase):

    def test__archive__symbols(self):
        self.assertIs(archive.Archive, archive.archive_.Archive)

    def test__file__symbols(self):
        self.assertIs(archive.ArchiveFile, archive.file_.ArchiveFile)

    def test__metadata__symbols(self):
        self.assertIs(archive.ArchiveMetadata, archive.metadata_.ArchiveMetadata)


if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
