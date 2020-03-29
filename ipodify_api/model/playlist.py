# -*- coding: utf-8 -*-
"""Playlist model objects package."""
import enum

from . import Hasheable


class PlaylistVisibility(enum.Enum):
    """Playlist visibility options class."""

    PRIVATE = "private"


class Playlist(Hasheable):
    """Playlist entity class."""

    def __init__(self, name, owner, visibility=PlaylistVisibility.PRIVATE, song_filter=None):
        """Create playlist entity."""
        self.__name = name
        self.__owner = owner
        self.__visibility = visibility
        self.__song_filter = song_filter

    @property
    def name(self):
        """Get playlist name."""
        return self.__name

    @property
    def owner(self):
        """Get playlist owner."""
        return self.__owner

    @property
    def visibility(self):
        """Get playlist visibility."""
        return self.__visibility

    @visibility.setter
    def visibility(self, visibility):
        """Set playlist visibility."""
        self.__visibility = visibility

    @property
    def song_filter(self):
        """Get playlist songs filter."""
        return self.__song_filter

    @song_filter.setter
    def song_filter(self, song_filter):
        """Set playlist songs filter."""
        self.__song_filter = song_filter

    @property
    def id(self):
        """Get playlist id."""
        return self.__owner.id + ':' + self.__name

    @property
    def __dict__(self):
        """Get dict representation of the playlist."""
        return {
            'name': self.__name,
            'owner': self.__owner.__dict__,
            'visibility': self.__visibility,
            # 'filter': self.__song_filter.__dict__
        }

    def __repr__(self):
        """Get string representation of the playlist."""
        return str(self.__dict__)
