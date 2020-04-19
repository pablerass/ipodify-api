# -*- coding: utf-8 -*-
"""Ports required by ipodify api service."""
from flask import request
from functools import wraps

from ..model import Hasheable

import requests


class SpotifyNotAuthenticatedError(Exception):
    """Error returned when not authenticated to Spotify or with invalid access token."""

    pass


# TUNE: Maybe this object should be moved to model
class SpotifyUser(Hasheable):
    """Spotify user."""

    def __init__(self, name, authorization):
        """Create Spotify user with its authorization header."""
        self.__name = name
        self.__authorization = authorization

    @property
    def name(self):
        """Get user name."""
        return self.__name

    @property
    def authorization(self):
        """Get user authorization header."""
        return self.__authorization

    def __hash__(self):
        """Return hash."""
        return hash(self.__name)


def spotify_auth(spotify_gateway):
    """Get requests SpotifyUser to be injected in the request handler."""
    def caller(func):
        @wraps(func)
        def wrapper(*kargs, **kwargs):
            authorization = request.headers.get('Authorization', '')
            try:
                spotify_user = spotify_gateway.get_user(authorization)
            except SpotifyNotAuthenticatedError:
                return {"message": "Not authenticated or authorization"}, 401
            return func(spotify_user, *kargs, **kwargs)
        return wrapper
    return caller


class SpotifyGateway(object):
    """Port to interact with Spotify service."""

    def __init__(self, url="https://api.spotify.com"):
        """Create a Spotify port with specific url."""
        self.__url = url

    @property
    def url(self):
        """Return Spotify url used."""
        return self.__url

    def get_user(self, authorization):
        """Get SpotifyUser."""
        authorization_header = {'Authorization': authorization}
        me = f"{self.__url}/v1/me"
        r = requests.get(me, headers=authorization_header)
        if r.status_code == 401:
            raise SpotifyNotAuthenticatedError()
        r.raise_for_status()
        return SpotifyUser(r.json()['id'], authorization)

    def get_library_tracks(self, spotify_user):
        """Get Spotify user tracks in library."""
        authorization_header = {'Authorization': spotify_user.authorization}
        limit = 50
        next_page_url = f"{self.__url}/v1/me/tracks?offset=0&limit={limit}"
        while next_page_url is not None:
            response = requests.get(next_page_url, headers=authorization_header)
            response.raise_for_status()
            response_content = response.json()
            next_page_url = response_content.get('next', None)
            for item in response_content.get('items'):
                yield item.get('track')

    def get_album(self, spotify_user, album_id):
        """Get an album with Spotify user credentials."""
        return self.get_albums(spotify_user, [album_id])

    def get_albums(self, spotify_user, album_ids):
        """Get multiple albums with Spotify user credentials."""
        authorization_header = {'Authorization': spotify_user.authorization}
        limit = 20
        for album_set_ids in (album_ids[i:i + limit] for i in range(0, len(album_ids), limit)):
            request_url = f"{self.__url}/v1/albums?ids={','.join(album_set_ids)}"
            response = requests.get(request_url, headers=authorization_header)
            response.raise_for_status()
            response_content = response.json()
            for item in response_content.get('albums'):
                yield item

    def get_artist(self, spotify_user, artist_id):
        """Get an artist with Spotify user credentials."""
        return self.get_artists(spotify_user, [artist_id])

    def get_artists(self, spotify_user, artist_ids):
        """Get multiple artists with Spotify user credentials."""
        authorization_header = {'Authorization': spotify_user.authorization}
        limit = 50
        for artist_set_ids in (artist_ids[i:i + limit] for i in range(0, len(artist_ids), limit)):
            request_url = f"{self.__url}/v1/artists?ids={','.join(artist_set_ids)}"
            response = requests.get(request_url, headers=authorization_header)
            response.raise_for_status()
            response_content = response.json()
            for item in response_content.get('artists'):
                yield item
