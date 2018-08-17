# -*- coding: utf8 -*-
"""Provides the Action class
"""

import abc

__all__ = ('Action',)


class Action(metaclass=abc.ABCMeta):
    """An abstract base class for actions"""

    __slots__ = ()

    @abc.abstractmethod
    def perform(self, subject):
        """Perform this action on the subject provided"""
        pass

    def __call__(self, subject):
        """Performs an action on the subject"""
        return self.perform(subject)


# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
