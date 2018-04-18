# -*- coding: utf8 -*-

from .. import util
from . import file_

import tempfile
import tarfile
import json
import os
import io

__all__ = ('Archive',)


class Archive:

    __slots__ = ('_tarfile', '_meta', '_tmpdir')

    _tarfile_attributes = (#'add',
                           'addfile',
                           #'bz2open',
                           'chmod',
                           'chown',
                           'closed',
                           'copybufsize',
                           'debug',
                           'dereference',
                           'encoding',
                           'errorlevel',
                           'errors',
                           'extract',
                           'extractall',
                           'extractfile',
                           'fileobj',
                           'fileobject',
                           'format',
                           'getmember',
                           'getmembers',
                           'getnames',
                           'gettarinfo',
                           #'gzopen',
                           'ignore_zeros',
                           'inodes',
                           'list',
                           'makedev',
                           'makedir',
                           'makefifo',
                           'makefile',
                           'makelink',
                           'makeunknown',
                           'members',
                           'mode',
                           'name',
                           'next',
                           'offset',
                           #'open',
                           'pax_headers',
                           'tarinfo',
                           #'taropen',
                           'utime',
                           #'xzopen'
                           )

    def __init__(self, tarfile, tmpdir=None, **kw):
        self._tarfile = tarfile
        self._tmpdir = tmpdir
        self._meta = kw.get('meta', dict())
        self._meta['graph'] = kw.get('graph', self._meta.get('graph'))
        self._meta['subdir'] = kw.get('subdir', self._meta.get('subdir', '.'))
        self._meta['files'] = kw.get('files', self._meta.get('files', dict()))

##        self._graph = kw.get('graph')
##        self._files = kw.get('files', dict())
##        self._init_tmpdir(kw.get('tmpdir', {'prefix': 'dsklayout-'}))
##        self._saved = False

##    def save(self):
##        self._save_metadata()
##        tar.add(self.tmpdir.name, os.path.basename(self.tmpdir.name))
##        self._saved = True

    def close(self):
        self.tarfile.close()
##        self._cleanup_tmpdir()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
##            if not self.saved:
##                self.save()
            self.close()
        return False

    def __getattr__(self, name):
        if name in self._tarfile_attributes:
            return getattr(self.tarfile, name)
        raise KeyError("%s object has no attribute %s" %
                       (repr(self.__class__.__name__), repr(name)))

    @property
    def tarfile(self):
        return self._tarfile

    @property
    def meta(self):
        return self._meta

    @property
    def graph(self):
        return self._meta['graph']

    @property
    def subdir(self):
        return self._meta['subdir']

##    @property
##    def files(self):
##        """Registered files (a dictionary of)"""
##        return self._meta['files']

    @property
    def tmpdir(self):
        """Optional temporary directory for importing/extracting on-disk files"""
        return self._tmpdir

    @property
    def saved(self):
        return self._saved

    def register_file(self, fileobj, key=None):
        self.files[(key or fileobj.path)] = fileobj

    def dump_attributes(self):
        return {'meta': util.dump_object(self.meta)}

    @classmethod
    def load_attributes(cls, attributes):
        return cls(**util.load_object(attributes['meta']))

    @classmethod
    def open(cls, name, mode='r', **kw):
        options = cls._extract_tar_options(kw)
        return cls(tarfile.open(name, mode, **options), **kw)

    @classmethod
    def _extract_tar_options(cls, kw):
        try:
            options = kw['options']
            del kw['options']
        except KeyError:
            options = dict()
        if 'format' not in options:
            options['format'] = tarfile.USTAR_FORMAT
        return options

    def add(name, arcname=None, *args, **kw):
        if arcname is None:
            arcname = os.path.join(self.subdir, name)
        meta = kw.get('meta', {'type': 'file'})
        self.meta['files'][name] = meta
        return self.tarfile.add(name, *args, **kw)

##    def _init_tmpdir(self, args):
##        if not isinstance(args, dict):
##            args = {'prefix': args}
##        self._tmpdir = tempfile.TemporaryDirectory(**args)

##    def _cleanup_tmpdir(self):
##        if self._tmpdir is not None:
##            self._tmpdir.cleanup()
##            self._tmpdir = None

##    def _save_metadata(self, filename='metadata.json'):
##        filepath = os.path.join(self.tmpdir.name, filename)
##        meta = {'type': 'dsklayout-metadata'}
##        self.register_file(file_.ArchiveFile(filename, meta))
##        with open(filepath, 'wt') as f:
##            f.write(json.dumps(util.dump_object(self), indent='  '))

    def _add_metadata_json(self, filename='metadata.json'):
        string = json.dumps(util.dump_object(self), indent='  ')
        content = string.encode("utf-8")
        name = os.path.join(self.subdir, filename)
        tarinfo = tarfile.TarInfo(name)
        tarinfo.size = len(content)
        self.addfile(tarinfo, io.BytesIO(content))

    def _add_tmpdir(self, metadata='metadata.json'):
        if isinstance(self.tmpdir, str) and os.path.exists(self.tmpdir):
            self.add(self.tmpdir, arcname=self.subdir,
                    filter=lambda ti : self._add_filter(ti, metadata))

    def _add_filter(self, tarinfo, metadata='metadata.json'):
        return tarinfo


# vim: set ft=python et ts=4 sw=4:
