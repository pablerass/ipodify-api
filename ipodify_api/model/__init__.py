# -*- coding: utf-8 -*-
"""Base model package with shared abstract classes."""
from abc import ABCMeta, abstractmethod


class Hasheable(metaclass=ABCMeta):
    """Hasheable abstract class definition."""

    @property
    @abstractmethod
    def id(self):
        """Return id to generate its hash."""
        pass

    def __hash__(self):
        """Return hash."""
        return hash(self.id)

    def __eq__(self, other):
        """Reqturn equal function."""
        if isinstance(other, self.__class__):
            return self.id == other.id
        return NotImplemented


class JSONSerializable(metaclass=ABCMeta):
    """JSON serialiable abstract class definition."""

    @abstractmethod
    def toJSON(self):
        """Convert to json string."""
        pass

    @abstractmethod
    def fromJSON(self):
        """Create object from json string."""
        pass
