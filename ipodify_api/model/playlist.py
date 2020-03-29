# -*- coding: utf-8 -*-
import enum

from . import Hasheable, JSONSerializable

from .song import SongFilter
from .user import User


class PlaylistVisibility(enum.Enum):
    PRIVATE = "private"


class Playlist(Hasheable):
    def __init__(self, name: str, owner: User, visibility = PlaylistVisibility.PRIVATE, song_filter = None):
        self.__name = name
        self.__owner = owner
        self.__visibility = visibility
        self.__song_filter = song_filter

    @property
    def __dict__(self):
        return {
            'name': self.__name,
            'owner': self.__owner.__dict__,
            'visibility': self.__visibility,
            #'filter': self.__song_filter.__dict__
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
    def song_filter(self):
        return self.__song_filter

    @song_filter.setter
    def song_filter(self, song_filter):
        self.__song_filter = song_filter

    @property
    def id(self):
        return self.__owner.id + ':' + self.__name
