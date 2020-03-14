# -*- coding: utf-8 -*-
"""ipodify api use cases."""
import logging

from .model.playlist import Playlist
from .model.user import User
from .ports import SpotifyUser


class LoggingUseCase(object):
    """Base use case class that supports logging."""

    def __init__(self):
        """Create logging use case."""
        self.__logger = logging.getLogger(f"use_cases.{self.__class__.__name__}")

    @property
    def logger(self):
        """Get logger."""
        return self.__logger


class PersistenceUseCase(LoggingUseCase):
    """Base use case that supports persisted entities."""

    def __init__(self, repository):
        """Create persisntece use case."""
        self.__repository = repository

    @property
    def repository(self):
        """Get repository."""
        return self.__repository

    def get_user(self, user_name):
        """Get user from its name."""
        # TODO: Move self creation to repository?
        try:
            user = self.repository.find_by_id(User, user_name)
        except KeyError:    # Replace this error for non specific repositry implementation one
            user = User(user_name)
            self.repository.add(user)

        return user


class GetUserLibraryUseCase(LoggingUseCase):
    """Get user library use case."""

    def __init__(self, spotify_port):
        """Create get library use case."""
        super().__init__()
        self.__spotify_port = spotify_port

    def execute(self, spotify_user: SpotifyUser):
        """Execute use case."""
        # Switch this to return songs
        tracks = []
        for track in self.__spotify_port.get_library(spotify_user):
            album = track.get('album')
            artists = track.get('artists')
            filtered_track = {
                'spotify_href': track.get('href'),
                'spotify_uri': track.get('uri'),
                'name': track.get('name'),
                'isrc': track.get('external_ids').get('isrc'),
                'release_date': album.get('release_date'),
                'album': album.get('name'),
                'artists': [a.get('name') for a in artists]
            }
            tracks.append(filtered_track)

        return tracks


class GetUserPlaylistsUseCase(PersistenceUseCase):
    """Get user playlists use case."""

    def execute(self, user_name):
        """Execute use case."""
        # TODO: Shoulf security be only implemented in use case level?
        user = self.get_user(user_name)
        playlists = self.repository.find_by_filter(Playlist, {"owner": user})

        return playlists


class AddPlaylistUseCase(PersistenceUseCase):
    """Add playlist use case."""

    def execute(self, user_name, playlist_name):
        """Execute use case."""
        user = self.get_user(user_name)
        playlist = Playlist(playlist_name, user)
        self.repository.add(playlist)
        return playlist


class GetPlaylistUseCase(PersistenceUseCase):
    """Get playlist use case."""

    def execute(self, user_name, playlist_name):
        """Execute use case."""
        user = self.get_user(user_name)
        playlists = self.repository.find_by_filter(Playlist, {"owner": user, "name": playlist_name})
        if not playlists:
            return {}
        return playlists[0]


class RemovePlaylistUseCase(PersistenceUseCase):
    """Remove playlist use case."""

    def execute(self, user_name, playlist_name):
        """Execute use case."""
        user = self.get_user(user_name)
        playlists = self.repository.find_by_filter(Playlist, {"owner": user, "name": playlist_name})
        if not playlists:
            return {}
        self.repository.remove(playlists[0])
        return playlists[0]
