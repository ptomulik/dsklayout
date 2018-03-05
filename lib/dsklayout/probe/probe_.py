# -*- coding: utf8 -*-

from .. import util
import abc

__all__ = ('Probe',)


class Probe(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def update_device(self, device):
        raise NotImplementedError("%s.update_device() not implemented for %s"
                                  % (self.__class__.__name__,
                                     type(device).__name__))

# vim: set ft=python et ts=4 sw=4:
