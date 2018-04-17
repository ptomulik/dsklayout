# -*- coding: utf8 -*-

from .. import util
from . import file_

import tempfile
import tarfile
import json
import os

__all__ = ('Archive',)


class Archive:

    __slots__ = ('_tarfile', '_options', '_graph', '_files', '_tmpdir', '_saved')

    def __init__(self, tarfile, **kw):
        self._tarfile = tarfile
        self._graph = kw.get('graph')
        self._files = kw.get('files', dict())
        self._init_tmpdir(kw.get('tmpdir', {'prefix': 'dsklayout-'}))
        self._saved = False

    def save(self):
        self._save_metadata()
        tar.add(self.tmpdir.name, os.path.basename(self.tmpdir.name))
        self._saved = True

    def close(self):
        self.tarfile.close()
        self._cleanup_tmpdir()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            if not self.saved:
                self.save()
            self.close()
        return False

    @property
    def tarfile(self):
        return self._tarfile

    @property
    def closed(self):
        return self.tarfile.closed

    @property
    def format(self):
        return self.tarfile.format

    @property
    def name(self):
        return self.tarfile.name

    @property
    def mode(self):
        return self.tarfile.mode

    @property
    def offset(self):
        return self.tarfile.offset

    @property
    def graph(self):
        return self._graph

    @property
    def files(self):
        """Registered files (a dictionary of)"""
        return self._files

    @property
    def tmpdir(self):
        """Temporary directory (an object) where we collect archive files"""
        return self._tmpdir

    @property
    def options(self):
        """Options for tarfile.open()"""
        return self._options

    @property
    def saved(self):
        return self._saved

    def register_file(self, fileobj, key=None):
        self.files[(key or fileobj.path)] = fileobj

    def dump_attributes(self):
        return {'graph': util.dump_object(self.graph),
                'files': util.dump_object(self.files)}

    @classmethod
    def load_attributes(cls, attributes):
        kw = {'graph': util.load_object(attributes['graph']),
              'files': util.load_object(attributes['files'])}
        return cls(**kw)

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

    def _init_tmpdir(self, args):
        if not isinstance(args, dict):
            args = {'prefix': args}
        self._tmpdir = tempfile.TemporaryDirectory(**args)

    def _cleanup_tmpdir(self):
        if self._tmpdir is not None:
            self._tmpdir.cleanup()
            self._tmpdir = None

    def _save_metadata(self, filename='metadata.json'):
        filepath = os.path.join(self.tmpdir.name, filename)
        meta = {'type': 'dsklayout-metadata'}
        self.register_file(file_.ArchiveFile(filename, meta))
        with open(filepath, 'wt') as f:
            f.write(json.dumps(util.dump_object(self), indent='  '))

# vim: set ft=python et ts=4 sw=4:
