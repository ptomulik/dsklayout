# -*- coding: utf8 -*-

from .. import util

__all__ = ()


def rekey_pt(ent, pt_map, pt_p_map, exclude=()):
    """Normalize keys in a partition table entry.

    This is used by :class:`.FdiskProbe` and :class:`.SfdiskProbe`.

    :param dict ent:
        input partition table,
    :param dict pt_map:
        field mappings for partition table metadata,
    :param dict pt_p_map:
        field mappings for partition metadata,
    :param exclude:
        fields to be excluded when processing **ent**.
    :return:
        a dictionary with "normalized" keys.
    :rtype: dict
    """
    def rkp(p): return dict(util.rekey(p, pt_p_map))
    pt = dict(util.rekey(ent, pt_map, ('partitions', *exclude)),
              partitions=list(rkp(p) for p in ent['partitions']))
    return pt


# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
