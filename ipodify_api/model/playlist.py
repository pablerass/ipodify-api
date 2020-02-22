# -*- coding: utf-8 -*-

from typing import List

from . import Hasheable
from .user import User


class PlaylistFilter(Hasheable):
    pass


class Playlist(Hasheable):
    def __init__(self, name: str, user: User, filters: List[PlaylistFilter] = None):
        self.__user = user
        self.__name = name
        if filters is None:
            self.__filters = []

    def __dict__(self):
        return {
            'name': self.__name,
            'filters': self.__filters
        }

    def __repr__(self):
        return str(self.__dict__())

    @property
    def name(self):
        return self.__name

    @property
    def user(self):
        return self.__user

    @property
    def id(self):
        return self.user.id + ':' + self.__name

    @staticmethod
    def get_id(name, user: User):
        return Playlist(name, user).id
