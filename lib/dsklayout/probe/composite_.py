# -*- coding: utf8 -*-
"""Provides the CompositeProbe base class
"""

from . import probe_
from . import lsblk_
from .. import util

import abc

__all__ = ('CompositeProbe',)


class CompositeProbe(probe_.Probe, metaclass=abc.ABCMeta):
    """Base class for all composite "probe" classes.

    A composite "probe" encapsulates two or more other probes.
    """

    @classmethod
    @abc.abstractmethod
    def uses(cls, **kw):
        """A list of probe classes required by this composite probe.

        Classes from the :meth:`uses` list are examined by :meth:`available`
        for their availability.

        .. note::
            This method **must** be implemented in a subclass.

        :param \*\*kw:
            keyword arguments, **must** be same as the ones passed to
            :meth:`new`.
        :return:
            a list of probe classes used by this composite probe.
        :rtype:
            list
        """
        pass

    @classmethod
    def available(cls, **kw):
        """Check if the all the probes, we depend on, are available.

        :param \*\*kw:
            keyword arguments, **must** be same as keyword arguments for
            :meth:`run`.

        :return:
            ``True``, if the supporting executable is available; otherwise
            ``False``.
        """
        return all(p.available(**kw) for p in cls.uses(**kw))

    @classmethod
    def mk_uses(cls, internal, external, **kw):
        """Make list of required probes.

        This utility method helps implementing :meth:`uses` in subclasses.
        The returned list contains all classes from **internal** and all
        classes from **external** that are not found in **\*\*kw**.

        :param list(type) internal:
            basic list of probe classes, which are always created internally by
            the subclass,
        :param dict external:
            a dictionary of probe classes, that are possibly provided via
            keyword arguments \*\*kw; the dictionary shall have form
            ``{key: klass}``, the ``klass`` is appended to the list of probes
            if ``key`` does not appear in **\*\*kw**.
        :return:
            a list of probe classes.
        :rtype: list
        """
        uses = internal[:]
        for key, klass in external.items():
            if key not in kw:
                uses.append(klass)
        return uses

    @classmethod
    def extract_lsblk_graph(cls, arguments, flags, kw):
        try:
            graph = kw['lsblkgraph']
            del kw['lsblkgraph']
        except KeyError:
            graph = lsblk_.LsBlkProbe.new(arguments, flags, **kw).graph()
        return graph

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
