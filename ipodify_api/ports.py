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
    def __init__(self, url="https://api.spotify.com", get_limit=50):
        self.__url = url
        self.__get_limit = get_limit

    def get_me(self, authorization):
        authorization_header = {'Authorization': authorization}
        me = f"{self.__url}/v1/me"
        r = requests.get(me, headers=authorization_header)
        if r.status_code == 401:
            raise SpotifyNotAuthenticatedError()
        r.raise_for_status()
        return SpotifyUser(r.json()['id'], authorization)

    def get_library(self, spotify_user):
        authorization_header = {'Authorization': spotify_user.authorization}
        next_page = f"{self.__url}/v1/me/tracks?offset=0&limit={self.__get_limit}"
        while next_page is not None:
            response = requests.get(next_page, headers=authorization_header)
            response.raise_for_status()
            response_content = response.json()
            next_page = response_content.get('next', None)
            for item in response_content.get('items'):
                yield item.get('track')
