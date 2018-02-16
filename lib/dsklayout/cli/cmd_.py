# -*- coding: utf8 -*-
"""`dsklayout.cli.cmd_`
"""

__all__ = ('Cmd',)

class Cmd(object):

    __slots__ = ('_parent',)

    def __init__(self, parent = None):
        if parent is not None:
            self._parent = parent
        super().__init__()
        self.add_arguments()

    def add_arguments(self):
        pass

    @property
    def parent(self):
        return self._parent

    @property
    def argparser(self):
        return self.parent.argparser

    @property
    def arguments(self):
        return self.parent.arguments


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
