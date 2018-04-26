# -*- coding: utf8 -*-
"""Provides the Cmd class
"""

__all__ = ('Cmd',)


class Cmd:

    __slots__ = ('_arguments',)

    def __init__(self, arguments=None):
        self._arguments = arguments or dict()

    @property
    def arguments(self):
        return self._arguments

    def argument(self, name):
        return self.argument[name]

    def getargument(self, name, default=None):
        return self.arguments.get(name, default)



# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
