# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class Hasheable(metaclass=ABCMeta):
    @property
    @abstractmethod
    def id(self):
        pass

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        return NotImplemented


class JSONSerializable(metaclass=ABCMeta):
    @abstractmethod
    def toJSON(self):
        pass

    @abstractmethod
    def fromJSON(self):
        pass