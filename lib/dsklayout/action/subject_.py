# -*- coding: utf8 -*-
"""Provides the ActionSubject class
"""

import abc

__all__ = ('ActionSubject',)


class ActionSubject(object, metaclass=abc.ABCMeta):
    """A base class for action subjects"""

    __slots__ = ()

    def accept_action(self, action):
        return action(self)


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
