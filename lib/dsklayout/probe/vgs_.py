# -*- coding: utf8 -*-

from . import backtick_
import json

__all__ = ('VgsProbe', )


class VgsProbe(backtick_.BackTickProbe):

    @classmethod
    def command(cls, **kw):
        return kw.get('vgs', 'vgs')

    @classmethod
    def flags(cls, flags, **kw):
        return ['--readonly', '--reportformat', 'json', '-o', '+vg_all'] + flags

    @classmethod
    def parse(cls, output):
        return json.loads(output)

# vim: set ft=python et ts=4 sw=4:
