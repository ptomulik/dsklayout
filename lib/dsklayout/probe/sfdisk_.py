# -*- coding: utf8 -*-

from . import backtick_
import json

__all__ = ('Sfdisk',)


class Sfdisk(backtick_.BackTick):

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
