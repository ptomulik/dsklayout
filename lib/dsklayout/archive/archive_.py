# -*- coding: utf8 -*-

from .. import util
from . import metadata_

import zipfile
import json
import os
import io

__all__ = ('Archive',)


class Archive:
    """Dsklayout archive.

    Physically, a saved archive is a zip archive containing several files. One
    of these files is a json file storing metadata for the application. Other
    in-archive files may be used directly by external tools, such as ``sfdisk``
    or ``sgdisk``, to restore certain parts of disk layout.

    In addition to members documented here, the class also exposes most of the
    methods and attributes provided by the :class:`zipfile.ZipFile`.

    Objects of :class:`.Archive` may be used as context managers.
    """

    __slots__ = ('_zipfile', '_metadata', '_metafile', '_lastmeta')

    _default_metafile = 'metadata.json'

    _zipfile_attributes = ('comment',
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
        """
        :param zipfile.ZipFile zipfile:
            an object implementing basic operations on the archive file,
        :param .ArchiveMetadata|None metadata:
            archive metadata to be stored in the metadata file,
        :keyword str metafile:
            optional file name of the in-archive metadata file.
        """
        self._zipfile = zipfile
        self.metafile = kw.get('metafile', self._default_metafile)
        self._init_lastmeta()
        self._init_metadata(metadata)

    def close(self):
        """Close the archive file with :meth:`zipfile.close
        <zipfile.ZipFile.close>`.

        If the archive is open for writing, the :attr:`.metadata` is written to
        the :attr:`metadata file <.metafile>` (``"metadata.json"`` by default)
        just before closing the archive.
        """
        if self.mode in ('a', 'x', 'w'):
            self.write_metadata(self.metadata)
        self.zipfile.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            if self.fp is not None:
                self.close()
        return False

    def __getattr__(self, name):
        if name in self._zipfile_attributes:
            return getattr(self.zipfile, name)
        raise KeyError("%s object has no attribute %s" %
                       (repr(self.__class__.__name__), repr(name)))

    @property
    def zipfile(self):
        """ZipFile object used to operate on the archive file.

        :rtype: zipfile.ZipFile
        """
        return self._zipfile

    @property
    def metadata(self):
        """Metadata object describing archive contents.

        :rtype: .ArchiveMetadata
        """
        return self._metadata

    @property
    def metafile(self):
        """Name of the in-archive file containing metadata.

        :rtype: str
        """
        return self._metafile

    @metafile.setter
    def metafile(self, filename):
        self._metafile = filename

    @property
    def lastmeta(self):
        """Last version of metadata found in the :attr:`metadata file
        <.metafile>`.

        This read-only property is updated internally. For an :class:`.Archive`
        instance created from scratch it's ``None``. For an :class:`.Archive`
        loaded from an archive file, it encapsulates the metadata loaded from
        in-archive :attr:`metadata file <.metafile>`. Every time the
        :attr:`.metadata` is saved to metadata file, the :attr:`.lastmeta` is
        updated to encapsulate a copy of the just-written :attr:`.metadata`.

        .. warning::
                Do not modify the object referenced by :attr:`.lastmeta`.

        :rtype: .ArchiveMetadata
        """
        return self._lastmeta

    @classmethod
    def new(cls, file, mode='r', **kw):
        """Create new :class:`.Archive` instance.

        This method accepts all arguments (positional and keyword arguments) of
        :class:`zipfile.ZipFile` constructor. Additional arguments to the
        constructor of :class:`.Archive` may be passed via keyword arguments.

        :returns: new instance of :class:`.Archive`
        :rtype: Archive
        """
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

    def _init_lastmeta(self):
        if self.mode in ('a', 'r'):
            self._lastmeta = self.read_metadata()
        else:
            self._lastmeta = None

    def _init_metadata(self, metadata):
        if not metadata and self._lastmeta:
            self._metadata = self._lastmeta.copy()
        else:
            self._metadata = metadata
        if not self._metadata:
            self._metadata = metadata_.ArchiveMetadata()

    def write_metadata(self, metadata, arcname=None):
        """Write metadata file to the archive file.

        :param ArchiveMetadata metadata:
            the metadata to be saved,
        :param str|None arcname:
            optional name of the in-archive destination file for metadata.
        """
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
        """Read metadata from file.

        :param str|None arcname:
            optional name of the in-archive source file containing metadata,
        :param str encoding:
            character encoding used to read the file.

        :returns: and instance of :class:`.ArchiveMetadata` loaded from the
                  file.
        :rtype: ArchiveMetadata
        """
        if arcname is None:
            arcname = self.metafile
        try:
            content = self.read(arcname)
        except KeyError:
            return None
        else:
            string = content.decode(encoding)
        return util.load_object(json.loads(string))

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
