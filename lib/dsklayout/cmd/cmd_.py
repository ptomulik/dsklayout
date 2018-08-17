# -*- coding: utf8 -*-
"""Provides the Cmd class
"""

__all__ = ('Cmd', 'ARGABSENT')

class _ArgAbsent: pass
ARGABSENT = _ArgAbsent()

class Cmd:

    __slots__ = ('_args',)

    def __init__(self, args=None):
        self._args = args or dict()

    @property
    def args(self):
        return self._args

    def arg(self, name):
        return self.args[name]

    def getarg(self, name, default=None):
        return self.args.get(name, default)

    def mapargs(self, mappings, defaults=None, default=ARGABSENT):
        if defaults is None:
            defaults = dict()
        mapped = {k: self.getarg(mappings[k], defaults.get(k, default))
                  for k in mappings}
        return {k: v for k, v in mapped.items() if v is not ARGABSENT}



# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
