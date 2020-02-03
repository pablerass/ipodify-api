# -*- coding: utf-8 -*-


class RequestUser(object):
    def __init__(self, name, auth_header):
        self.__name = name
        self.__auth_header = auth_header

    @property
    def name(self):
        return self.__name

    @property
    def auth_header(self):
        return self.__auth_header


class UserCollection(object):
    def __init__(self):
        self.__users = {}

    def load_user(self, user_name):
        if user_name not in self.__users:
            self.__users[user_name] = User(user_name)
        return self.__users[user_name]


class User(object):
    def __init__(self, name, playlists=None):
        self.__name = name
        if playlists is None:
            self.__playlists = set()
        else:
            self.__playlists = playlists

    @property
    def name(self):
        return self.__name

    @property
    def playlists(self):
        return self.__playlists

    def add_playlist(self, playlist):
        self.__playlists.add(playlist)

    def remove_playlist(self, playlist):
        self.__playlists.remove(playlist)
