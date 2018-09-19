# -*- coding: utf8 -*-
"""Archive implementation.

This module provides objects used to export and import dsklayout data. In the
centre, there is a class named :class:`.Archive`, which encapsulates complete
information about disk layout. The content of :class:`.Archive` can be easily
saved to an archive file. The file may be later read by application yielding,
again, an instance of :class:`.Archive`.
"""

from .. import util
util.import_all_from(__package__, [
    '.archive_',
    '.metadata_',
    '.file_'
    ])

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
