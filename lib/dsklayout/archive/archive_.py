# -*- coding: utf8 -*-

from .. import util

import tempfile
import tarfile
import os

__all__ = ('Archive',)


class Archive:

    __slots__ = ('_path', '_options', '_graph', '_files', '_tmpdir')

    def __init__(self, path, **kw):
        self._path = path
        self._init_options(kw.get('options', dict()))
        self._graph = kw.get('graph')
        self._files = kw.get('files', dict())
        self._init_tmpdir(kw.get('tmpdir', {'dir': 'dsklayout'}))


    def __enter__(self):
        return self

    def __exit__(self, exc_type exc_val, exc_tb):
        return False

    @property
    def graph(self):
        return self._graph

    @property
    def files(self):
        return self._files

    @property
    def tmpdir(self):
        return self._tmpdir

    @property
    def options(self):
        return self._options

    def add_file(self, file, key=None):
        self.files[(key or file.path)] = file

    def dump_attributes(self):
        return {'graph': util.dump_object(self.graph),
                'files': util.dump_object(self.files)}

    @classmethod
    def load_attributes(cls, attributes):
        kw = {'graph': util.load_object(attributes['graph']),
              'files': util.load_object(attributes['files'])}
        return cls(**kw)

    def _init_tmpdir(self, args):
        if not isinstance(args, dict):
            args = {'dir': args}
        self._tmpdir = tempfile.TemporaryDirectory(**tmpdir)

    def _init_options(self, options):
        if 'format' not in options:
            options['format'] = tarfile.USTAR_FORMAT
        self._options = options

    def _pack_tmpdir(self):
        with tarfile.open(self.path, 'w:gz', **self.options) as tar:
            tar.add(self.tmpdir, os.path.basename(self.tmpdir))


# vim: set ft=python et ts=4 sw=4:
