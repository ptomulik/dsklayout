# -*- coding: utf8 -*-
"""Provides the Action class
"""

import abc

__all__ = ('Action',)


class Action(object, metaclass=abc.ABCMeta):
    """An abstract base class for actions"""

    __slots__ = ()

    @property
    @abc.abstractmethod
    def method(self):
        """Name of the subject's method to be invoked by this action"""
        pass

    def __call__(self, subject):
        """Dispatch to appropriate method of the subject"""
        return getattr(subject, self.method)(self)


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
