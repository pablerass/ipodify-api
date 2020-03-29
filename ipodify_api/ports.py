# -*- coding: utf-8 -*-
import requests


class SpotifyNotAuthenticatedError(Exception):
    pass


class SpotifyUser(object):
    def __init__(self, name, authorization):
        self.__name = name
        self.__authorization = authorization

    @property
    def name(self):
        return self.__name

    @property
    def authorization(self):
        return self.__authorization


class SpotifyPort(object):
    def __init__(self, url="https://api.spotify.com"):
        self.__url = url

    def get_user(self, authorization):
        authorization_header = {'Authorization': authorization}
        me = f"{self.__url}/v1/me"
        r = requests.get(me, headers=authorization_header)
        if r.status_code == 401:
            raise SpotifyNotAuthenticatedError()
        r.raise_for_status()
        return SpotifyUser(r.json()['id'], authorization)

    def get_library_tracks(self, spotify_user):
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
        return self.get_albums(spotify_user, [album_id])

    def get_albums(self, spotify_user, album_ids):
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
        return self.get_artists(spotify_user, [artist_id])

    def get_artists(self, spotify_user, artist_ids):
        authorization_header = {'Authorization': spotify_user.authorization}
        limit = 50
        for artist_set_ids in (artist_ids[i:i + limit] for i in range(0, len(artist_ids), limit)):
            request_url = f"{self.__url}/v1/artists?ids={','.join(artist_set_ids)}"
            response = requests.get(request_url, headers=authorization_header)
            response.raise_for_status()
            response_content = response.json()
            for item in response_content.get('artists'):
                yield item
