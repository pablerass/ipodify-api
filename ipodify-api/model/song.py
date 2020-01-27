# -*- coding: utf-8 -*-


class SongSource(object):
    def __init__(self, service, uri, href=None, url=None):
        self.__service = service
        self.__uri = uri
        self.__href = href
        self.__url = url

    @property
    def service(self):
        return self.__service

    @property
    def uri(self):
        return self.__uri

    @property
    def href(self):
        return self.__href

    @property
    def url(self):
        return self.__url

    def __dict__(self):
        d = {
            'service': self.__service,
            'uri': self.__uri,
        }
        if not self.__href is None:
            d.update({
                'href': self.__href
            })
        if not self.__url is None:
            d.update({
                'url': self.__url
            })

    def __key(self):
        return (self.__service, self.__uri)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__key() == other.__key()
        return NotImplemented


class SongFactory(object):
    @staticmethod
    def from_spotify_track(spotify_track_dict):
        track = spotify_track_dict
        album = track.get('album')
        track = {
            'sources': [
                SongSource('spotify', uri=track.get('uri'), href=track.get('href'),
                           url=track.get('external_urls').get('spotify'))
            ]
            'name': track.get('name'),
            'isrc': track.get('external_ids').get('isrc'),
            'country': track.get('external_ids').get('isrc')[0:2],
            'release_date': album.get('release_date'),
            'album': album.get('name')
        }
        return Song(**track)


class Song(object):
    def __init__(self, name, isrc, release_date, album, country, genres=None, sources=None):
        pass