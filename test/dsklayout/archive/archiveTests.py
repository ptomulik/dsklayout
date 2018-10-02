#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import unittest.mock as mock
from unittest.mock import patch

import dsklayout.archive.archive_ as archive_

class Test__Archive(unittest.TestCase):

    @property
    def zipfile_attributes(self):
        return ('comment',
                'compression',
                'debug',
                'extract',
                'extractall',
                'filelist',
                'filename',
                'fp',
                'getinfo',
                'infolist',
                'mode',
                'namelist',
                'open',
                'printdir',
                'pwd',
                'read',
                'setpassword',
                'start_dir',
                'testzip',
                'write',
                'writestr')

    def test__init__1(self):
        f = mock.Mock(spec=True)
        with patch.object(archive_.Archive, '_init_lastmeta') as init_lastmeta, \
             patch.object(archive_.Archive, '_init_metadata') as init_metadata:
            arch = archive_.Archive(f)
            self.assertIs(arch._zipfile, f)
            self.assertIs(arch._metafile, archive_.Archive._default_metafile)
            init_lastmeta.assert_called_once_with()
            init_metadata.assert_called_once_with(None)

    def test__init__2(self):
        f = mock.Mock(spec=True)
        m = mock.Mock(spec=True)
        with patch.object(archive_.Archive, '_init_lastmeta') as init_lastmeta, \
             patch.object(archive_.Archive, '_init_metadata') as init_metadata:
            arch = archive_.Archive(f, m)
            self.assertIs(arch._zipfile, f)
            self.assertIs(arch._metafile, archive_.Archive._default_metafile)
            init_lastmeta.assert_called_once_with()
            init_metadata.assert_called_once_with(m)

    def test__init__3(self):
        f = mock.Mock(spec=True)
        m = mock.Mock(spec=True)
        mf = mock.Mock(spec=True)
        with patch.object(archive_.Archive, '_init_lastmeta') as init_lastmeta, \
             patch.object(archive_.Archive, '_init_metadata') as init_metadata:
            arch = archive_.Archive(f, m, metafile=mf)
            self.assertIs(arch._zipfile, f)
            self.assertIs(arch._metafile, mf)
            init_lastmeta.assert_called_once_with()
            init_metadata.assert_called_once_with(m)

    def test__zipfile(self):
        f = mock.Mock(spec=True)
        with patch.object(archive_.Archive, '_init_lastmeta') as init_lastmeta, \
             patch.object(archive_.Archive, '_init_metadata') as init_metadata:
            arch = archive_.Archive(f)
            self.assertIs(arch.zipfile, arch._zipfile)
            arch._zipfile = None
            self.assertIsNone(arch.zipfile)

    def test__metadata(self):
        f = mock.Mock(spec=True)
        m = mock.Mock(spec=True)
        with patch.object(archive_.Archive, '_init_lastmeta') as init_lastmeta, \
             patch.object(archive_.Archive, '_init_metadata') as init_metadata:
            arch = archive_.Archive(f)
            arch._metadata = m
            self.assertIs(arch.metadata, arch._metadata)

    def test__metafile(self):
        f = mock.Mock(spec=True)
        m = mock.Mock(spec=True)
        with patch.object(archive_.Archive, '_init_lastmeta') as init_lastmeta, \
             patch.object(archive_.Archive, '_init_metadata') as init_metadata:
            arch = archive_.Archive(f)
            arch._metafile = m
            self.assertIs(arch.metafile, arch._metafile)

    def test__lastmeta(self):
        f = mock.Mock(spec=True)
        m = mock.Mock(spec=True)
        with patch.object(archive_.Archive, '_init_lastmeta') as init_lastmeta, \
             patch.object(archive_.Archive, '_init_metadata') as init_metadata:
            arch = archive_.Archive(f)
            arch._lastmeta = m
            self.assertIs(arch.lastmeta, arch._lastmeta)

    def test__getattr__1(self):
        f = mock.Mock()
        for attr in self.zipfile_attributes:
            setattr(f, attr, ('ok %s' % attr))

        with patch.object(archive_.Archive, '_init_lastmeta') as init_lastmeta, \
             patch.object(archive_.Archive, '_init_metadata') as init_metadata:
            arch = archive_.Archive(f)
            for attr in self.zipfile_attributes:
                self.assertEqual(getattr(arch, attr), ('ok %s' % attr))

    def test__getattr__2(self):
        f = mock.Mock(spec=True)
        with patch.object(archive_.Archive, '_init_lastmeta') as init_lastmeta, \
             patch.object(archive_.Archive, '_init_metadata') as init_metadata:
            arch = archive_.Archive(f)
            with self.assertRaises(AttributeError) as context:
                arch.foo
            self.assertEqual(str(context.exception), "%s object has no attribute %s" % (repr(arch.__class__.__name__), repr('foo')))

    def test__enter__(self):
        f = mock.Mock(spec=True)
        with patch.object(archive_.Archive, '_init_lastmeta') as init_lastmeta, \
             patch.object(archive_.Archive, '_init_metadata') as init_metadata:
            arch = archive_.Archive(f)
            self.assertIs(arch.__enter__(), arch)

    def test__exit__1(self):
        f = mock.Mock(spec=True, fp=None)
        with patch.object(archive_.Archive, '_init_lastmeta') as init_lastmeta, \
             patch.object(archive_.Archive, '_init_metadata') as init_metadata, \
             patch.object(archive_.Archive, 'close') as close:
            arch = archive_.Archive(f)
            self.assertFalse(arch.__exit__(None, None, None))
            close.assert_not_called()

    def test__exit__2(self):
        f = mock.Mock(spec=True, fp=1)
        with patch.object(archive_.Archive, '_init_lastmeta') as init_lastmeta, \
             patch.object(archive_.Archive, '_init_metadata') as init_metadata, \
             patch.object(archive_.Archive, 'close') as close:
            arch = archive_.Archive(f)
            self.assertFalse(arch.__exit__(1, None, None))
            close.assert_not_called()

    def test__exit__2(self):
        f = mock.Mock(spec=True, fp=1)
        with patch.object(archive_.Archive, '_init_lastmeta') as init_lastmeta, \
             patch.object(archive_.Archive, '_init_metadata') as init_metadata, \
             patch.object(archive_.Archive, 'close') as close:
            arch = archive_.Archive(f)
            self.assertFalse(arch.__exit__(None, None, None))
            close.assert_called_once_with()

    def test__new__1(self):
        f = mock.Mock(spec=True, name='ZipFile')
        options = {'foo': 'FOO'}
        with patch('dsklayout.archive.archive_.Archive._extract_zip_options', return_value=options) as extract, \
             patch('zipfile.ZipFile', return_value = f) as ZipFile, \
             patch.object(archive_.Archive, '_init_lastmeta'), \
             patch.object(archive_.Archive, '_init_metadata'):
            arch = archive_.Archive.new('test.zip', bar='BAR')
            self.assertIs(arch.zipfile, f)
            self.assertIsInstance(arch, archive_.Archive)
            extract.assert_called_once_with({'bar': 'BAR'})
            ZipFile.assert_called_once_with('test.zip', 'r', **options)

    def test__new__2(self):
        f = mock.Mock(spec=True, name='ZipFile')
        options = {'foo': 'FOO'}
        with patch('dsklayout.archive.archive_.Archive._extract_zip_options', return_value=options) as extract, \
             patch('zipfile.ZipFile', return_value = f) as ZipFile, \
             patch.object(archive_.Archive, '_init_lastmeta'), \
             patch.object(archive_.Archive, '_init_metadata'):
            arch = archive_.Archive.new('test.zip', 'w', bar='BAR')
            self.assertIs(arch.zipfile, f)
            self.assertIsInstance(arch, archive_.Archive)
            extract.assert_called_once_with({'bar': 'BAR'})
            ZipFile.assert_called_once_with('test.zip', 'w', **options)


if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
