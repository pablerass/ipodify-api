# -*- coding: utf-8 -*-


class Playlist(object):
    # TODO: Make this class json serializable
    def __init__(self, name, filters=None):
        self.__name = name

    def __dict__(self):
        return {
            'name': self.__name,
        }

    def __key(self):
        return (self.__name)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__key() == other.__key()
        return NotImplemented


class PlaylistFilter(object):
    pass