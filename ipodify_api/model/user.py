# -*- coding: utf-8 -*-
"""User model objects package."""
from . import Identifiable


class User(Identifiable):
    """User entity class."""

    def __init__(self, name):
        """Create user entity."""
        self.__name = name

    @property
    def name(self):
        """Get user name."""
        return self.__name

    @property
    def id(self):
        """Get user id."""
        return self.__name

    @property
    def __dict__(self):
        """Get dict representation of the user."""
        return {
            'name': self.__name,
        }

    def __repr__(self):
        """Get string representation of the playlist."""
        return str(self.__dict__)
