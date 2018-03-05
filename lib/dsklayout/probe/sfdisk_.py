# -*- coding: utf8 -*-

from . import backtick_
from .. import util
import json

__all__ = ('SfdiskProbe',)


class SfdiskProbe(backtick_.BackTickProbe):

    @classmethod
    def command(cls, **kw):
        return kw.get('sfdisk', 'sfdisk')

    @classmethod
    def flags(cls, flags, **kw):
        return ['-J'] + flags

    @classmethod
    def parse(cls, output):
        return json.loads(output)


# vim: set ft=python et ts=4 sw=4:
