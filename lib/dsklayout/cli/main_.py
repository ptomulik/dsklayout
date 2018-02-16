# -*- coding: utf8 -*-
"""`dsklayout.cli.main_`

Provides the Main class
"""

import argparse
import sys

__all__ = ('Main',)

class Main(object):

    __slots__ = ('_argparser', )

    def __init__(self):
        self._argparser = argparse.ArgumentParser(
                description = 'Retrieve and backup layouts of block devices',
                usage = '''dsklayout <command> [<args>]
Commands:
    help        Print help and exit
''')

        self._argparser.add_argument('command', help='Subcommand to run')

    @property
    def argparser(self):
        return self._argparser

    def run(self):
        args = self.argparser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command) or args.command == 'run':
            sys.stderr.write('error: unrecognized command %r\n' % args.command)
            self.argparser.print_help()
            return 1
        return getattr(self, args.command)()

    def help(self):
        self.argparser.print_help()

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
