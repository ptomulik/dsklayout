# -*- coding: utf8 -*-

from . import backtick_
import json

__all__ = ('LvsProbe', )


class LvsProbe(backtick_.BackTickProbe):

    @classmethod
    def command(cls, **kw):
        return kw.get('lvs', 'lvs')

    @classmethod
    def flags(cls, flags, **kw):
        return ['--readonly', '--reportformat', 'json', '-o', '+lv_all'] + flags

    @classmethod
    def parse(cls, output):
        return json.loads(output)

# vim: set ft=python et ts=4 sw=4:
