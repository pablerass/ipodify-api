# -*- coding: utf-8 -*-
"""Playlist model objects package."""
import enum

from . import Identifiable


class PlaylistVisibility(enum.Enum):
    """Playlist visibility options class."""

    PRIVATE = "private"


class Playlist(Identifiable):
    """Playlist entity class."""

    def __init__(self, name, owner, track_filter, visibility=PlaylistVisibility.PRIVATE):
        """Create playlist entity."""
        self.__name = name
        self.__owner = owner
        self.__visibility = visibility
        self.__track_filter = track_filter

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
    def track_filter(self):
        """Get playlist tracks filter."""
        return self.__track_filter

    @track_filter.setter
    def track_filter(self, track_filter):
        """Set playlist tracks filter."""
        self.__track_filter = track_filter

    @property
    def id(self):
        """Get playlist id."""
        return self.__owner.id + ':' + self.__name

    @property
    def __dict__(self):
        """Get dict representation of the playlist."""
        return {
            'name': self.__name,
            'owner': self.__owner.name,
            'visibility': self.__visibility.value,
            'track_filter': self.__track_filter.__dict__
        }

    def __repr__(self):
        """Get string representation of the playlist."""
        return str(self.__dict__)
