# -*- coding: utf-8 -*-
"""Song model objects package."""
from abc import ABCMeta, abstractmethod

import json
import operator as ops
import re

from . import Hasheable, JSONSerializable


class InvalidOperatorException(Exception):
    """Exception raise when filter object created with an invalid operator."""

    pass


class InvalidFilterException(Exception):
    """Exception raise when filter object does not work properly with an invalid operator."""

    pass


class InvalidJsonSongFilterException(Exception):
    """Exception raise when a json string is not a valid song filter representation."""

    pass


class SongFilter(Hasheable, JSONSerializable, metaclass=ABCMeta):
    """Abstract song filter class."""

    @staticmethod
    @abstractmethod
    def _managed_operators():
        pass

    @abstractmethod
    def match(self, song):
        """Return if the song matches against the filter."""
        pass

    def toJSON(self):
        """Convert to json string."""
        return json.dumps(self.__dict__)

    @staticmethod
    def _decompose_filter(filter_dict):
        if len(filter_dict) != 1:
            raise InvalidJsonSongFilterException(f"{filter_dict} has more than one key")
        operator = list(filter_dict)[0]
        value = filter_dict[operator]
        return operator, value

    @classmethod
    def fromJSON(cls, json_string):
        """Create object from json string."""
        return cls.fromDict(json.loads(json_string))

    @classmethod
    def fromDict(cls, filter_dict):
        return cls._fromComponents(*cls._decompose_filter(filter_dict))

    @classmethod
    @abstractmethod
    def _fromComponents(cls, operator, value):
        for _class in cls.__subclasses__():
            if operator in _class._managed_operators():
                return _class._fromComponents(operator, value)
        raise InvalidJsonSongFilterException()

    def __hash__(self):
        """Return hash."""
        return hash(self.toJSON())

    @property
    @abstractmethod
    def __dict__(self):
        """Return dict representation of the object."""
        pass


# TODO: Add class to composite playlists
# class SongInsidePlaylistFilter(SongFiler):


class SongPropertyFilter(SongFilter):
    """Song filter that matches a song property to a value with an operator."""

    @staticmethod
    def _managed_operators():
        return ["$eq", "$ne", "$gt", "$lt", "$le", "$ge", "$match", "$nmatch", "$in", "$ni"]

    def __init__(self, operator, song_property, value):
        """Create song property filter."""
        if operator not in self._managed_operators():
            raise InvalidOperatorException(f"{operator} is not a valid single song filter operator")

        if operator in ["$eq", "$ne", "$gt", "$lt", "$le", "$ge"]:
            self.__method = getattr(ops, operator.lstrip('$'))
            if operator == "$ne":
                self.__list_method = all
            else:
                self.__list_method = any
        elif operator == "$match":
            # TODO: Raise exception if value is not a valid regex
            self.__method = lambda sp, regex: bool(re.match(regex, sp))
            self.__list_method = any
        elif operator == "$nmatch":
            # TODO: Raise exception if value is not a valid regex
            self.__method = lambda sp, regex: not bool(re.match(regex, sp))
            self.__list_method = all
        elif operator == "$in":
            # TODO: Raise exception if value is not a list
            self.__method = lambda sp, value_list: sp in value_list
            self.__list_method = any
        elif operator == "$ni":
            # TODO: Raise exception if value is not a list
            self.__method = lambda sp, value_list: sp not in value_list
            self.__list_method = all
        else:
            raise InvalidFilterException(f"{operator} is a valid operator but it is not properly handled")

        self.__operator = operator
        self.__song_property = song_property
        self.__value = value

    def match(self, song):
        """Return if the song matches against the filter."""
        # TODO: Make comparisons lowercase and ignoring accents when strings
        # TODO: Raise exception if "gt", "lt", "le", "ge" operations are executed againsts list properties
        property_value = getattr(song, self.__song_property)
        if not isinstance(property_value, list):
            return self.__method(property_value, self.__value)
        else:
            return self.__list_method([self.__method(v, self.__value) for v in property_value])

    @classmethod
    def _fromComponents(cls, operator, value):
        return cls(operator, *cls._decompose_filter(value))

    @property
    def __dict__(self):
        """Return dict representation of the object."""
        return {self.__operator: {self.__song_property: self.__value}}


class SongAggregateFilter(SongFilter):
    """Song filter that aggregates multiple song filters with an operator."""

    @staticmethod
    def _managed_operators():
        return ["$and", "$or"]

    def __init__(self, operator, song_filters):
        """Create song filter that aggregates other filters."""
        if operator not in self._managed_operators():
            raise InvalidOperatorException(f"{operator} is not a valid aggregate song filter operator")

        if operator == "$and":
            self.__method = all
        elif operator == "$or":
            self.__method = any
        else:
            raise InvalidFilterException(f"{operator} is a valid operator but it is not properly handled")
        self.__operator = operator
        self.__song_filters = song_filters

    def match(self, song):
        """Return if the song matches against the filter."""
        return self.__method([f.match(song) for f in self.__song_filters])

    @classmethod
    def _fromComponents(cls, operator, value):
        return cls(operator, [SongFilter.fromDict(d) for d in value])

    @property
    def __dict__(self):
        """Return dict representation of the object."""
        return {self.__operator: [f.__dict__ for f in self.__song_filters]}


class SongNotFilter(SongFilter):
    """Song filter that negates other song filter."""

    @staticmethod
    def _managed_operators():
        return ["$not"]

    def __init__(self, song_filter):
        """Create song filter negation filter."""
        self.__song_filter = song_filter

    def match(self, song):
        """Return if the song matches against the filter."""
        return not self.__song_filter.match(song)

    @classmethod
    def _fromComponents(cls, operator, value):
        return cls(SongFilter.fromDict(value))

    @property
    def __dict__(self):
        """Return dict representation of the object."""
        return {"$not": self.__song_filter.__dict__}


class Song(object):
    """Song entity class."""

    def __init__(self, name, isrc, album, release_year, language, artists, genres):
        """Create song entity."""
        self.__name = name
        self.__isrc = isrc
        self.__album = album
        self.__release_year = release_year
        self.__language = language
        self.__artists = artists
        if not isinstance(self.__artists, list):
            self.__artists = [self.__artists]
        self.__genres = genres
        if self.__genres is None:
            self.__genres = []

    def match_filter(self, song_filter):
        """Check if the song matches against a filter."""
        return song_filter.match(self)

    @property
    def name(self):
        """Get song name."""
        return self.__name

    @property
    def isrc(self):
        """Get song ISRC."""
        return self.__isrc

    @property
    def album(self):
        """Get song album."""
        return self.__album

    @property
    def release_year(self):
        """Get song release year."""
        return self.__release_year

    @property
    def language(self):
        """Get song language."""
        return self.__language

    @property
    def artists(self):
        """Get song artists."""
        return self.__artists

    @property
    def genres(self):
        """Get song genres."""
        return self.__genres

    @property
    def __dict__(self):
        """Get dict representation of the song."""
        return {
            "name": self.__name,
            "isrc": self.__isrc,
            "release_year": self.__release_year,
            "album": self.__album,
            "language": self.__language,
            "artists": self.__artists,
            "genres": self.__genres
        }


class SpotifySong(Song):
    """Song entity class with references to internal Spotify id."""

    def __init__(self, uri, href, name, isrc, album, release_year, language, artists, genres):
        """Create Spotify song entity."""
        self.__uri = uri
        self.__href = href
        super().__init__(name, isrc, album, release_year, language, artists, genres)

    @property
    def uri(self):
        """Get Spotify song uri."""
        return self.__uri

    @property
    def href(self):
        """Get Spotify song href."""
        return self.__href

    @property
    def __dict__(self):
        """Get dict representation of the Spotify song."""
        super_dict = super().__dict__
        super_dict.update({
            "uri": self.__uri,
            "href": self.__href
        })
        return super_dict
