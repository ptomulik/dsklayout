# -*- coding: utf8 -*-

from .. import util
util.import_all_from(__package__, [
    '.app_',
    '.backupcmd_',
    '.cmd_',
    '.cmdbase_',
    '.dotcmd_',
    '.dsklayout_',
    '.ext_',
    '.fdiskext_',
    '.lsblkext_',
    '.mdadmext_',
    '.sfdiskext_',
    '.tmpdirext_',
    '.vgcfgbackupext_',
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
