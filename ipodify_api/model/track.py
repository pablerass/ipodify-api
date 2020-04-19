# -*- coding: utf-8 -*-
"""Track model objects package."""
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


class InvalidJsonTrackFilterException(Exception):
    """Exception raise when a json string is not a valid track filter representation."""

    pass


# TODO: Track filter could be generalized as property filter
class TrackFilter(Hasheable, JSONSerializable, metaclass=ABCMeta):
    """Abstract track filter class."""

    @staticmethod
    @abstractmethod
    def _managed_operators():
        pass

    @abstractmethod
    def match(self, track):
        """Return if the track matches against the filter."""
        pass

    def toJSON(self):
        """Convert to json string."""
        return json.dumps(self.__dict__)

    @staticmethod
    def _decompose_filter(filter_dict):
        if len(filter_dict) != 1:
            raise InvalidJsonTrackFilterException(f"{filter_dict} has more than one key")
        operator = list(filter_dict)[0]
        value = filter_dict[operator]
        return operator, value

    @classmethod
    def fromJSON(cls, json_string):
        """Create object from json string."""
        return cls.fromDict(json.loads(json_string))

    @classmethod
    def fromDict(cls, filter_dict):
        """Create object from dict."""
        return cls._fromComponents(*cls._decompose_filter(filter_dict))

    @classmethod
    @abstractmethod
    def _fromComponents(cls, operator, value):
        for _class in cls.__subclasses__():
            if operator in _class._managed_operators():
                return _class._fromComponents(operator, value)
        raise InvalidJsonTrackFilterException()

    def __hash__(self):
        """Return hash."""
        return hash(self.toJSON())

    @property
    @abstractmethod
    def __dict__(self):
        """Return dict representation of the object."""
        pass


# TODO: Add class to composite playlists
# class TrackInsidePlaylistFilter(TrackFiler):


class TrackPropertyFilter(TrackFilter):
    """Track filter that matches a track property to a value with an operator."""

    @staticmethod
    def _managed_operators():
        return ["$eq", "$ne", "$gt", "$lt", "$le", "$ge", "$match", "$nmatch", "$in", "$ni"]

    def __init__(self, operator, track_property, value):
        """Create track property filter."""
        if operator not in self._managed_operators():
            raise InvalidOperatorException(f"{operator} is not a valid single track filter operator")

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
        self.__track_property = track_property
        self.__value = value

    def match(self, track):
        """Return if the track matches against the filter."""
        # TODO: Make comparisons lowercase and ignoring accents when strings
        # TODO: Raise exception if "gt", "lt", "le", "ge" operations are executed againsts list properties
        property_value = getattr(track, self.__track_property)
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
        return {self.__operator: {self.__track_property: self.__value}}


class TrackAggregateFilter(TrackFilter):
    """Track filter that aggregates multiple track filters with an operator."""

    @staticmethod
    def _managed_operators():
        return ["$and", "$or"]

    def __init__(self, operator, track_filters):
        """Create track filter that aggregates other filters."""
        if operator not in self._managed_operators():
            raise InvalidOperatorException(f"{operator} is not a valid aggregate track filter operator")

        if operator == "$and":
            self.__method = all
        elif operator == "$or":
            self.__method = any
        else:
            raise InvalidFilterException(f"{operator} is a valid operator but it is not properly handled")
        self.__operator = operator
        self.__track_filters = track_filters

    def match(self, track):
        """Return if the track matches against the filter."""
        return self.__method([f.match(track) for f in self.__track_filters])

    @classmethod
    def _fromComponents(cls, operator, value):
        return cls(operator, [TrackFilter.fromDict(d) for d in value])

    @property
    def __dict__(self):
        """Return dict representation of the object."""
        return {self.__operator: [f.__dict__ for f in self.__track_filters]}


class TrackNotFilter(TrackFilter):
    """Track filter that negates other track filter."""

    @staticmethod
    def _managed_operators():
        return ["$not"]

    def __init__(self, track_filter):
        """Create track filter negation filter."""
        self.__track_filter = track_filter

    def match(self, track):
        """Return if the track matches against the filter."""
        return not self.__track_filter.match(track)

    @classmethod
    def _fromComponents(cls, operator, value):
        return cls(TrackFilter.fromDict(value))

    @property
    def __dict__(self):
        """Return dict representation of the object."""
        return {"$not": self.__track_filter.__dict__}


class Track(object):
    """Track entity class."""

    def __init__(self, name, isrc, album, release_year, language, artists, genres):
        """Create track entity."""
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

    def match_filter(self, track_filter):
        """Check if the track matches against a filter."""
        return track_filter.match(self)

    @property
    def name(self):
        """Get track name."""
        return self.__name

    @property
    def isrc(self):
        """Get track ISRC."""
        return self.__isrc

    @property
    def album(self):
        """Get track album."""
        return self.__album

    @property
    def release_year(self):
        """Get track release year."""
        return self.__release_year

    @property
    def language(self):
        """Get track language."""
        return self.__language

    @property
    def artists(self):
        """Get track artists."""
        return self.__artists

    @property
    def genres(self):
        """Get track genres."""
        return self.__genres

    @property
    def __dict__(self):
        """Get dict representation of the track."""
        return {
            "name": self.__name,
            "isrc": self.__isrc,
            "release_year": self.__release_year,
            "album": self.__album,
            "language": self.__language,
            "artists": self.__artists,
            "genres": self.__genres
        }


class SpotifyTrack(Track):
    """Track entity class with references to internal Spotify id."""

    def __init__(self, uri, href, name, isrc, album, release_year, language, artists, genres):
        """Create Spotify track entity."""
        self.__uri = uri
        self.__href = href
        super().__init__(name, isrc, album, release_year, language, artists, genres)

    @property
    def uri(self):
        """Get Spotify track uri."""
        return self.__uri

    @property
    def href(self):
        """Get Spotify track href."""
        return self.__href

    @property
    def __dict__(self):
        """Get dict representation of the Spotify track."""
        super_dict = super().__dict__
        super_dict.update({
            "uri": self.__uri,
            "href": self.__href
        })
        return super_dict
