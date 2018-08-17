# -*- coding: utf8 -*-
"""Provides the Probe base class
"""

__all__ = ('Probe',)


class Probe:
    """Base class for all "probe" classes.

    A "probe" object encapsulates data obtainted by querying operating system.
    This is usually done by runing external program or several related
    programs."""

    __slots__ = ('_content',)

    def __init__(self, content):
        """Initializes the Probe."""
        self._content = content

    @property
    def content(self):
        """Data encapsulated by this object. Type, syntax and semantics of the
        content is specified by a subclass."""
        return self._content

    def dump_attributes(self):
        """Supports serialization."""
        return {'content': self.content}

    @classmethod
    def load_attributes(cls, attributes):
        """Supports deserialization."""
        return cls(attributes['content'])



# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
