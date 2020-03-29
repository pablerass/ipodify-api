# -*- coding: utf-8 -*-

import operator as ops
import re

from abc import ABCMeta, abstractmethod


class InvalidOperatorException(Exception):
    pass


class SongFilter(object, metaclass=ABCMeta):
    @abstractmethod
    def match(self, song):
        pass


# TODO: Add class to composite playlists
#class SongInsidePlaylistFilter(SongFiler):


class SongPropertyFilter(SongFilter):
    def __init__(self, operator, song_property, value):
        if operator in ["eq", "ne", "gt", "lt", "le", "ge"]:
            self.__method = getattr(ops, operator)
            if operator == "ne":
                self.__list_method = all
            else:
                self.__list_method = any
        elif operator == "match":
            # TODO: Raise exception if value is not a valid regex
            self.__method = lambda sp, regex: bool(re.match(regex, sp))
            self.__list_method = any
        elif operator == "nmatch":
            # TODO: Raise exception if value is not a valid regex
            self.__method = lambda sp, regex: not bool(re.match(regex, sp))
            self.__list_method = all
        elif operator == "in":
            # TODO: Raise exception if value is not a list
            self.__method = lambda sp, value_list: sp in value_list
            self.__list_method = any
        elif operator == "ni":
            # TODO: Raise exception if value is not a list
            self.__method = lambda sp, value_list: sp not in value_list
            self.__list_method = all
        else:
            raise InvalidOperatorException(f"{operator} is not a valid single song filter operator")
        self.__operator = operator
        self.__song_property = song_property
        self.__value = value

    def match(self, song):
        # TODO: Make comparisons lowercase and ignoring accents when strings
        # TODO: Raise exception if "gt", "lt", "le", "ge" operations are executed againsts list properties
        property_value = getattr(song, self.__song_property)
        if not isinstance(property_value, list):
            return self.__method(property_value, self.__value)
        else:
            return self.__list_method([self.__method(v, self.__value) for v in property_value])


class SongAggregateFilter(SongFilter):
    def __init__(self, operator, song_filters):
        if operator == "and":
            self.__method = all
        elif operator == "or":
            self.__method = any
        else:
            raise InvalidOperatorException(f"{operator} is not a valid aggregate song filter operator")
        self.__operator = operator
        self.__song_filters = song_filters

    def match(self, song):
        return self.__method([f.match(song) for f in self.__song_filters])


class SongNotFilter(SongFilter):
    def __init__(self, song_filter):
        self.__song_filter = song_filter

    def match(self, song):
        return not self.__song_filter.match(song)


class Song(object):
    def __init__(self, name, isrc, album, release_year, language, artists, genres):
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
        return song_filter.match(self)

    @property
    def name(self):
        return self.__name

    @property
    def isrc(self):
        return self.__isrc

    @property
    def album(self):
        return self.__album

    @property
    def release_year(self):
        return self.__release_year

    @property
    def language(self):
        return self.__language

    @property
    def artists(self):
        return self.__artists

    @property
    def genres(self):
        return self.__genres

    @property
    def __dict__(self):
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
    def __init__(self, uri, href, name, isrc, album, release_year, language, artists, genres):
        self.__uri = uri
        self.__href = href
        super().__init__(name, isrc, album, release_year, language, artists, genres)

    @property
    def uri(self):
        return self.__uri

    @property
    def href(self):
        return self.__href

    @property
    def __dict__(self):
        super_dict = super().__dict__
        super_dict.update({
            "uri": self.__uri,
            "href": self.__href
        })
        return super_dict

    # TODO: Implement full equal
