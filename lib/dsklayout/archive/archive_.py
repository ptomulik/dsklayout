# -*- coding: utf8 -*-

from .. import util
from . import metadata_

import zipfile
import json
import os
import io

__all__ = ('Archive',)


class Archive:

    __slots__ = ('_zipfile', '_metadata', '_metafile', '_lastmeta')

    _default_metafile = 'metadata.json'

    _zipfile_attributes = ('close',
                           'comment',
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

    def __init__(self, zipfile, metadata=None, **kw):
        self._zipfile = zipfile
        self.metafile = kw.get('metafile', self._default_metafile)
        self._init_metadata(metadata)

    def close(self):
        if self.mode in ('a', 'x', 'w'):
            self.write_metadata(self.metadata)
        self.zipfile.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            if not self.closed:
                self.close()
        return False

    def __getattr__(self, name):
        if name in self._zipfile_attributes:
            return getattr(self.zipfile, name)
        raise KeyError("%s object has no attribute %s" %
                       (repr(self.__class__.__name__), repr(name)))

    @property
    def zipfile(self):
        """TarFile object"""
        return self._zipfile

    @property
    def metadata(self):
        """Metadata object describing archive contents"""
        return self._metadata

    @property
    def metafile(self):
        """In-archive file containing metadata"""
        return self._metafile

    @metafile.setter
    def metafile(self, filename):
        self._metafile = filename

    @property
    def lastmeta(self):
        return self._lastmeta

    @classmethod
    def new(cls, file, mode='r', **kw):
        options = cls._extract_zip_options(kw)
        return cls(zipfile.ZipFile(file, mode, **options), **kw)

    @classmethod
    def _extract_zip_options(cls, kw):
        options = dict()
        for key in ('compression', 'allowZip64'):
            try:
                options[key] = kw[key]
                del kw[key]
            except KeyError:
                pass
        return options

    def _init_metadata(self, metadata):
        if self.mode in ('a', 'r'):
            self._lastmeta = self.read_metadata()
        else:
            self._lastmeta = None
        if not metadata and self._lastmeta:
            self._metadata = self._lastmeta.copy()
        else:
            self._metadata = metadata
        if not self._metadata:
            self._metadata = metadata_.ArchiveMetadata()

    def write_metadata(self, metadata, arcname=None):
        if arcname is None:
            arcname = self.metafile
        array = util.dump_object(metadata)
        lastarray = util.dump_object(self.lastmeta)
        if array == lastarray:
            return
        string = json.dumps(array, indent='  ')
        self.writestr(arcname, string)
        self._lastmeta = self.metadata.copy()

    def read_metadata(self, arcname=None, encoding='utf-8'):
        if arcname is None:
            arcname = self.metafile
        try:
            content = self.read(arcname)
        except KeyError:
            return None
        else:
            string = content.decode(encoding)
        return util.load_object(json.loads(string))

# vim: set ft=python et ts=4 sw=4:
