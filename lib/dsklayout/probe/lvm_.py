# -*- coding: utf8 -*-

from . import lvs_
from . import vgs_
from . import pvs_

__all__ = ('LvmProbe',)


class LvmProbe(probe_.Probe):

    @classmethod
    @abc.abstractmethod
    def parse(cls, output):
        """Parse output retrieved from the external program"""
        pass

    @classmethod
    def new(cls, arguments=None, flags=None, **kw):
        """Creates a new instance of LvmProbe for specified arguments by
           running and interpreting output of external command."""
# How to determine from arguments which devices should be included? It's gonna
# work only with lsblk graph.
##        lvs = lvs_.LvsProbe.new(arguments, flags, **kw)
##        vgs = vgs_.PvsProbe.new(arguments, flags, **kw)
##        pvs = pvs_.PvsProbe.new(arguments, flags, **kw)
        content = {}
        return cls(content)

# vim: set ft=python et ts=4 sw=4:
