# -*- coding: utf-8 -*-
"""ipodify api use cases."""
import logging
import requests

from . import constants
from .model.user import User
from .model.playlist import Playlist


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


def filter_track(track):
    """Filter Spotify track content to fix out song model."""
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
    return filtered_track


class GetUserLibraryUseCase(LoggingUseCase):
    """Get user library use case."""

    def __init__(self, spotify_api_url=constants.SPOTIFY_API_URL):
        """Create get library use case."""
        super().__init__()
        self.__spotify_api_url = spotify_api_url

    def execute(self, user):
        """Execute use case."""
        tracks = []
        next_page = f"{self.__spotify_api_url}/v1/me/tracks?offset=0&limit={constants.SPOTIFY_LIMIT}"
        while next_page is not None:
            r = requests.get(next_page, headers=user.auth_header)
            r_content = r.json()
            r.raise_for_status()
            tracks.extend([filter_track(t.get('track')) for t in r_content.get('items')])
            next_page = r_content.get('next', None)
            self.logger.debug(f"Obtained {r_content.get('limit')} from {r_content.get('offset')}")
        return {'tracks': tracks}


class AddPlaylistUseCase(PersistenceUseCase):
    """Add playlist use case."""

    def execute(self, user_name, playlist_name):
        """Execute use case."""
        user = self.get_user(user_name)
        self.repository.add(Playlist(playlist_name, user))


class GetUserPlaylistsUseCase(PersistenceUseCase):
    """Get user playlists use case."""

    def execute(self, user_name):
        """Execute use case."""
        # TODO: Shoulf security be only implemented in use case level?
        user = self.repository.find_by_id(User, user_name)
        playlists = self.repository.find_by_filter(Playlist, {"user": user})

        return playlists


class RemovePlaylistUseCase(PersistenceUseCase):
    """Remove playlist use case."""

    def execute(self, user_name, playlist_name):
        """Execute use case."""
        user = self.get_user(user_name)
        self.repository.remove_by_filter(Playlist, {"name": playlist_name, "user": user})
