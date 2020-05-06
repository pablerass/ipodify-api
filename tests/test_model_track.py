# -*- coding: utf-8 -*-
import pytest

import json

from ipodify_api.model.track import Track, TrackFilter, TrackAggregateFilter, TrackPropertyFilter, TrackNotFilter


def test_property_filters():
    track_params = {
        "name": "Blue (Da Ba Dee) - Gabry Ponte Ice Pop Radio",
        "isrc": "ITT019810102",
        "release_year": 2011,
        "album": "Europop",
        "language": "English",
        "artists": ["Eiffel 65", "Gabry Ponte"],
        "genres": ["bubblegum dance", "eurodance", "europop", "italian pop", "italo dance"]
    }
    track = Track(**track_params)

    filter_artists_eq = TrackPropertyFilter("$eq", "artists", "Eiffel 65")
    filter_artists_ne = TrackPropertyFilter("$ne", "artists", "Extremoduro")
    assert track.match_filter(filter_artists_eq)
    assert track.match_filter(filter_artists_ne)

    filter_name_match = TrackPropertyFilter("$match", "name", "^Blue .*$")
    filter_name_nmatch = TrackPropertyFilter("$nmatch", "name", "^Blue .*$")
    assert track.match_filter(filter_name_match)
    assert not track.match_filter(filter_name_nmatch)

    filter_genres_match1 = TrackPropertyFilter("$match", "genres", "^.*pop.*$")
    filter_genres_match2 = TrackPropertyFilter("$match", "genres", "^.*jazz.*$")
    assert track.match_filter(filter_genres_match1)
    assert not track.match_filter(filter_genres_match2)

    filter_album_in = TrackPropertyFilter("$in", "album", ["Europop", "Desaparecido"])
    filter_album_ni = TrackPropertyFilter("$ni", "album", ["Correos", "Donde están mis amigos"])
    assert track.match_filter(filter_album_in)
    assert track.match_filter(filter_album_ni)

    filter_artists_in = TrackPropertyFilter("$in", "artists", ["Eiffel 65", "Manu Chao"])
    filter_artists_ni1 = TrackPropertyFilter("$ni", "artists", ["Platero y Tú", "Extremoduro"])
    filter_artists_ni2 = TrackPropertyFilter("$ni", "artists", ["Gabry Ponte", "Extremoduro"])
    assert track.match_filter(filter_artists_in)
    assert track.match_filter(filter_artists_ni1)
    assert not track.match_filter(filter_artists_ni2)


def test_aggregate_filters():
    track_params = {
        "name": "Blue (Da Ba Dee) - Gabry Ponte Ice Pop Radio",
        "isrc": "ITT019810102",
        "release_year": 2011,
        "album": "Europop",
        "language": "English",
        "artists": ["Eiffel 65", "Gabry Ponte"],
        "genres": ["bubblegum dance", "eurodance", "europop", "italian pop", "italo dance"]
    }
    track = Track(**track_params)
    filter1 = TrackAggregateFilter("$and", [TrackPropertyFilter("$eq", "album", "Europop"),
                                           TrackPropertyFilter("$eq", "language", "English")])
    filter2 = TrackAggregateFilter("$or", [TrackPropertyFilter("$eq", "artists", "Eiffel 65"),
                                          TrackPropertyFilter("$eq", "language", "Spanish")])
    filter3 = TrackAggregateFilter("$and", [TrackPropertyFilter("$eq", "album", "Europop"),
                                           TrackPropertyFilter("$eq", "language", "Spanish")])
    not_filter3 = TrackNotFilter(filter3)
    assert track.match_filter(filter1)
    assert track.match_filter(filter2)
    assert not track.match_filter(filter3)
    assert track.match_filter(not_filter3)


def test_real_world_filters():
    track_params = {
        "name": "Blue (Da Ba Dee) - Gabry Ponte Ice Pop Radio",
        "isrc": "ITT019810102",
        "release_year": 2011,
        "album": "Europop",
        "language": "English",
        "artists": ["Eiffel 65", "Gabry Ponte"],
        "genres": ["bubblegum dance", "eurodance", "europop", "italian pop", "italo dance"]
    }
    track = Track(**track_params)
    decade_2000_filter = TrackAggregateFilter("$and", [TrackPropertyFilter("$ge", "release_year", 2000),
                                                      TrackPropertyFilter("$lt", "release_year", 2010)])
    decade_2010_filter = TrackAggregateFilter("$and", [TrackPropertyFilter("$ge", "release_year", 2010),
                                                      TrackPropertyFilter("$lt", "release_year", 2020)])
    assert not track.match_filter(decade_2000_filter)
    assert track.match_filter(decade_2010_filter)


def test_track_filter_json():
    composed_filter = TrackNotFilter(TrackAggregateFilter(
        "$and", [TrackPropertyFilter("$ge", "release_year", 2000),
                 TrackNotFilter(TrackPropertyFilter("$lt", "release_year", 2010))]))
    composed_filter_dict = {"$not": {"$and": [{"$ge": {"release_year": 2000}},
                                              {"$not": {"$lt": {"release_year": 2010}}}]}}
    assert composed_filter.__dict__ == composed_filter_dict
    assert TrackFilter.fromDict(composed_filter_dict).__dict__ == composed_filter_dict