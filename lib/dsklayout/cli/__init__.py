# -*- coding: utf8 -*-

from .. import util
util.import_all_from(__package__, [
    '.app_',
    '.backupcmd_',
    '.cmd_',
    '.cmdbase_',
    '.ext_',
    '.dsklayout_',
    '.lsblkext_',
    ])


def main():
    try:
        return DskLayout().run()
    except KeyboardInterrupt:
        return 0

# vim: set ft=python et ts=4 sw=4:
