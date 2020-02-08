# -*- coding: utf-8 -*-


class Playlist(object):
    # TODO: Make this class json serializable
    def __init__(self, name, filters=None):
        self.__name = name

    def __dict__(self):
        return {
            'name': self.__name,
        }

    @property
    def id(self):
        return (self.__name)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        return NotImplemented


class PlaylistFilter(object):
    pass
