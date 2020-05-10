# -*- coding: utf-8 -*-
"""User model objects package."""
from . import Identifiable


class User(Identifiable):
    """User entity class."""

    def __init__(self, name, playlists=None):
        """Create user entity."""
        if playlists is None:
            playlists = []

        self.__name = name
        self.__playlists = set(playlists)

    def add_playlist(self, playlist):
        """Add playlist to user."""
        self.__playlists.add(playlist)

    def remove_playlist(self, playlist):
        """Remove playlist from user."""
        self.__playlists.remove(playlist)

    @property
    def name(self):
        """Get user name."""
        return self.__name

    @property
    def playlists(self):
        """Get user playlists."""
        return sorted(list(self.__playlists), key=lambda p: p.id)

    @property
    def id(self):
        """Get user id."""
        return self.__name

    @property
    def __dict__(self):
        """Get dict representation of the user."""
        return {
            'name': self.__name
        }

    def __repr__(self):
        """Get string representation of the playlist."""
        return str(self.__dict__)
