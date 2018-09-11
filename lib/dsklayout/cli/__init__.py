# -*- coding: utf8 -*-
"""Command Line Interface
"""

from .. import util
util.import_all_from(__package__, [
    '.app_',
    '.backupcmd_',
    '.cmd_',
    '.cmdbase_',
    '.dotcmd_',
    '.dsklayout_',
    '.ext_',
    '.progext_',
    '.tmpdirext_',
    ])


def main():
    try:
        return DskLayout().run()
    except KeyboardInterrupt:
        return 0

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
