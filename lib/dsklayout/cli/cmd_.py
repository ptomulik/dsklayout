# -*- coding: utf8 -*-
"""`dsklayout.cli.cmd_`
"""

from . import cmdbase_

__all__ = ('Cmd',)

class Cmd(cmdbase_.CmdBase):
    """Base class for actual command (subcommand)"""

    __slots__ = ( '_arguments', '_extensions' )

    def __init__(self, **kw):
        super().__init__()
        self._extensions = kw.get('extensions', dict())

    @property
    def extensions(self):
        return self._extensions

    @property
    def properties(self):
        return dict()

    @property
    def arguments(self):
        return self._arguments

    @arguments.setter
    def arguments(self, arguments):
        self._arguments = arguments

    def __getattr__(self, name):
        try:
            return self._extensions[name]
        except KeyError:
            raise AttributeError(name)

    def add_extension(self, ext, name=None):
        if name is None:
            name = ext.name
        self._extensions[name] = ext
        ext.parent = self

    def add_arguments(self, parser):
        self.add_cmd_arguments(parser)
        self.add_ext_arguments(parser)

    def add_ext_arguments(self, parser):
        for key,ext in self._extensions.items():
            ext.add_arguments(parser)

    def set_defaults(self, parser):
        self.set_cmd_defaults(parser)
        self.set_ext_defaults(parser)

    def set_ext_defaults(self, parser):
        for key,ext in self._extensions.items():
            ext.set_defaults(parser)

    def add_cmd_arguments(self, parser):
        pass

    def set_cmd_defaults(self, parser):
        pass

    def run(self):
        return 0


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
