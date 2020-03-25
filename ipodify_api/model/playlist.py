# -*- coding: utf-8 -*-
import enum

from . import Hasheable
from .user import User


class PlaylistFilter():
    pass


class PlaylistVisibility(enum.Enum):
    PRIVATE = "private"


class Playlist(Hasheable):
    def __init__(self, name: str, owner: User, visibility: PlaylistVisibility = PlaylistVisibility.PRIVATE,
                 filter: PlaylistFilter = None):
        self.__name = name
        self.__owner = owner
        self.__visibility = visibility
        self.__filter = filter

    @property
    def __dict__(self):
        return {
            'name': self.__name,
            'owner': self.__owner.__dict__,
            'visibility': self.__visibility,
            #'filter': self.__filter.__dict__
        }

    def __repr__(self):
        return str(self.__dict__)

    @property
    def name(self):
        return self.__name

    @property
    def owner(self):
        return self.__owner

    @property
    def visibility(self):
        return self.__visibility

    @visibility.setter
    def visibility(self, visibility):
        self.__visibility = visibility

    @property
    def filter(self):
        return self.__filter

    @filter.setter
    def filter(self, filter):
        self.__filter = filter

    @property
    def id(self):
        return self.__owner.id + ':' + self.__name
