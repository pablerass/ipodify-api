# -*- coding: utf-8 -*-
import logging
import requests

from . import constants


class BaseUseCase(object):
    def __init__(self):
        self._logger = logging.getLogger(f"use_cases.{self.__class__.__name__}")


def filter_track(track):
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


class GetLibraryUseCase(BaseUseCase):
    def __init__(self, spotify_api_url=constants.SPOTIFY_API_URL):
        super().__init__()
        self.__spotify_api_url = spotify_api_url

    def execute(self, user):
        tracks = []
        next_page = f"{self.__spotify_api_url}/v1/me/tracks?offset=0&limit={constants.SPOTIFY_LIMIT}"
        while not next_page is None:
            r = requests.get(next_page, headers=user.auth_header)
            r_content = r.json()
            r.raise_for_status()
            tracks.extend([filter_track(t.get('track')) for t in r_content.get('items')])
            next_page = r_content.get('next', None)
            self._logger.debug(f"Obtained {r_content.get('limit')} from {r_content.get('offset')}")
        return {'tracks': tracks}


class GetPlaylistsUseCase(BaseUseCase):
    def __init__(self, user_collection):
        self.__user_collection = user_collection

    def execute(self, user_name):
        user = self.__user_collection.load_user(user_name)
        return user.playlists

class AddPlaylistUseCase(BaseUseCase):
    def __init__(self, user_collection):
        self.__user_collection = user_collection

    def execute(self, user_name, playlist):
        user = self.__user_collection.load_user(user_name)
        return user.add_playlist(playlist)

class RemovePlaylistUseCase(BaseUseCase):
    def __init__(self, user_collection):
        self.__user_collection = user_collection

    def execute(self, user_name, playlist):
        user = self.__user_collection.load_user(user_name)
        return user.remove_playlist(playlist)

