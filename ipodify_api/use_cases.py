# -*- coding: utf-8 -*-
"""ipodify api use cases."""
from collections import defaultdict
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

    @staticmethod
    def __language_from_isrc(isrc):
        # TODO: Find less dramatic way to obtain language
        if isrc is None:
            return 'Unknown'
        code = isrc[0:1]
        if code == 'ES':
            return 'Spanish'
        if code == 'FR':
            return 'French'
        return 'English'

    def execute(self, spotify_user: SpotifyUser):
        """Execute use case."""
        # TODO: Change this to return songs
        tracks = []
        albums_dict = defaultdict(list)
        artists_dict = defaultdict(list)
        for track in self.__spotify_port.get_library(spotify_user):
            album = track.get('album')
            artists = track.get('artists')
            filtered_track = {
                'uri': track.get('uri'),
                'name': track.get('name'),
                'isrc': track.get('external_ids').get('isrc'),
                'release_year': album.get('release_date').split('-')[0],
                'genres': [],   # Try to convert genres to set
                'language': self.__language_from_isrc(track.get('external_ids').get('isrc')),
                'album': album.get('name'),
                'album_uri': album.get('uri'),
                'artists': [a.get('name') for a in artists]
            }
            tracks.append(filtered_track)
            albums_dict[album.get('id')].append(filtered_track)
            for artist in artists:
                artists_dict[artist.get('id')].append(filtered_track)

        # TODO: Find a more accurate way to get genres
        for album in self.__spotify_port.get_albums(spotify_user, list(albums_dict.keys())):
            for track in albums_dict[album.get('id')]:
                track['genres'].extend([g for g in album.get('genres') if g not in track['genres']])

        for artist in self.__spotify_port.get_artists(spotify_user, list(artists_dict.keys())):
            for track in artists_dict[artist.get('id')]:
                track['genres'].extend([g for g in artist.get('genres') if g not in track['genres']])

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
