# -*- coding: utf-8 -*-
"""Base model package with shared abstract classes."""
from abc import ABCMeta, abstractmethod


class Hasheable(metaclass=ABCMeta):
    """Hasheable abstract class definition."""

    @abstractmethod
    def __hash__(self):
        """Return hash."""
        pass

    def __eq__(self, other):
        """Return equal function."""
        if isinstance(other, self.__class__):
            return self.__hash__() == other.__hash__()
        return NotImplemented


class Identifiable(Hasheable, metaclass=ABCMeta):
    """Identifiable abstract class definition."""

    @property
    def id(self):
        """Return id to generate its hash."""
        pass

    def __hash__(self):
        """Return hash."""
        return hash(self.id)
