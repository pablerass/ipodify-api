# -*- coding: utf-8 -*-
import pytest

import json

from ipodify_api.model.song import Song, SongFilter, SongAggregateFilter, SongPropertyFilter, SongNotFilter


def test_property_filters():
    song_params = {
        "name": "Blue (Da Ba Dee) - Gabry Ponte Ice Pop Radio",
        "isrc": "ITT019810102",
        "release_year": 2011,
        "album": "Europop",
        "language": "English",
        "artists": ["Eiffel 65", "Gabry Ponte"],
        "genres": ["bubblegum dance", "eurodance", "europop", "italian pop", "italo dance"]
    }
    song = Song(**song_params)

    filter_artists_eq = SongPropertyFilter("$eq", "artists", "Eiffel 65")
    filter_artists_ne = SongPropertyFilter("$ne", "artists", "Extremoduro")
    assert song.match_filter(filter_artists_eq)
    assert song.match_filter(filter_artists_ne)

    filter_name_match = SongPropertyFilter("$match", "name", "^Blue .*$")
    filter_name_nmatch = SongPropertyFilter("$nmatch", "name", "^Blue .*$")
    assert song.match_filter(filter_name_match)
    assert not song.match_filter(filter_name_nmatch)

    filter_genres_match1 = SongPropertyFilter("$match", "genres", "^.*pop.*$")
    filter_genres_match2 = SongPropertyFilter("$match", "genres", "^.*jazz.*$")
    assert song.match_filter(filter_genres_match1)
    assert not song.match_filter(filter_genres_match2)

    filter_album_in = SongPropertyFilter("$in", "album", ["Europop", "Desaparecido"])
    filter_album_ni = SongPropertyFilter("$ni", "album", ["Correos", "Donde están mis amigos"])
    assert song.match_filter(filter_album_in)
    assert song.match_filter(filter_album_ni)

    filter_artists_in = SongPropertyFilter("$in", "artists", ["Eiffel 65", "Manu Chao"])
    filter_artists_ni1 = SongPropertyFilter("$ni", "artists", ["Platero y Tú", "Extremoduro"])
    filter_artists_ni2 = SongPropertyFilter("$ni", "artists", ["Gabry Ponte", "Extremoduro"])
    assert song.match_filter(filter_artists_in)
    assert song.match_filter(filter_artists_ni1)
    assert not song.match_filter(filter_artists_ni2)


def test_aggregate_filters():
    song_params = {
        "name": "Blue (Da Ba Dee) - Gabry Ponte Ice Pop Radio",
        "isrc": "ITT019810102",
        "release_year": 2011,
        "album": "Europop",
        "language": "English",
        "artists": ["Eiffel 65", "Gabry Ponte"],
        "genres": ["bubblegum dance", "eurodance", "europop", "italian pop", "italo dance"]
    }
    song = Song(**song_params)
    filter1 = SongAggregateFilter("$and", [SongPropertyFilter("$eq", "album", "Europop"),
                                           SongPropertyFilter("$eq", "language", "English")])
    filter2 = SongAggregateFilter("$or", [SongPropertyFilter("$eq", "artists", "Eiffel 65"),
                                          SongPropertyFilter("$eq", "language", "Spanish")])
    filter3 = SongAggregateFilter("$and", [SongPropertyFilter("$eq", "album", "Europop"),
                                           SongPropertyFilter("$eq", "language", "Spanish")])
    not_filter3 = SongNotFilter(filter3)
    assert song.match_filter(filter1)
    assert song.match_filter(filter2)
    assert not song.match_filter(filter3)
    assert song.match_filter(not_filter3)


def test_real_world_filters():
    song_params = {
        "name": "Blue (Da Ba Dee) - Gabry Ponte Ice Pop Radio",
        "isrc": "ITT019810102",
        "release_year": 2011,
        "album": "Europop",
        "language": "English",
        "artists": ["Eiffel 65", "Gabry Ponte"],
        "genres": ["bubblegum dance", "eurodance", "europop", "italian pop", "italo dance"]
    }
    song = Song(**song_params)
    decade_2000_filter = SongAggregateFilter("$and", [SongPropertyFilter("$ge", "release_year", 2000),
                                                      SongPropertyFilter("$lt", "release_year", 2010)])
    decade_2010_filter = SongAggregateFilter("$and", [SongPropertyFilter("$ge", "release_year", 2010),
                                                      SongPropertyFilter("$lt", "release_year", 2020)])
    assert not song.match_filter(decade_2000_filter)
    assert song.match_filter(decade_2010_filter)


def test_song_filter_json():
    composed_filter = SongNotFilter(SongAggregateFilter(
        "$and", [SongPropertyFilter("$ge", "release_year", 2000),
                 SongNotFilter(SongPropertyFilter("$lt", "release_year", 2010))]))
    composed_filter_dict = {"$not": {"$and": [{"$ge": {"release_year": 2000}},
                                              {"$not": {"$lt": {"release_year": 2010}}}]}}
    assert composed_filter.__dict__ == composed_filter_dict
    assert composed_filter.toJSON() == json.dumps(composed_filter_dict)
    assert SongFilter.fromJSON(json.dumps(composed_filter_dict)) == composed_filter