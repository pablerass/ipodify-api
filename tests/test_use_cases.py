# -*- coding: utf-8 -*-
import os
import pytest

from ipodify_api.model.playlist import Playlist
from ipodify_api.model.user import User
from ipodify_api.model.song import SpotifySong

from ipodify_api.repositories.memory import MemoryRepository, filter_match

from ipodify_api.ports import SpotifyPort, SpotifyUser

from ipodify_api.use_cases import AddPlaylistUseCase, GetUserPlaylistsUseCase, RemovePlaylistUseCase, \
                                  GetUserLibraryUseCase


# TODO: Replace this by pytest-datadir or pytest-datafiles
@pytest.fixture
def content():
    def _get_content(file_name):
        file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures', 'use_cases', file_name)
        with open(file_path, 'r') as f:
            return f.read()

    return _get_content


@pytest.fixture
def repository():
    return MemoryRepository()


@pytest.fixture
def spotify_user():
    return SpotifyUser("user", "aaaaa")


def test_playlist_use_cases(repository):
    add_playlist = AddPlaylistUseCase(repository)
    get_playlists = GetUserPlaylistsUseCase(repository)
    remove_playlist = RemovePlaylistUseCase(repository)

    user_name = "a"
    playlist_name = "a"

    user = User(user_name)
    playlist = Playlist(playlist_name, user)

    add_playlist.execute(user_name, playlist_name)
    assert get_playlists.execute(user_name) == [playlist]
    remove_playlist.execute(user_name, playlist_name)
    assert get_playlists.execute(user_name) == []


def test_get_user_library_user_case(spotify_user, requests_mock, content):
    spotify_url = "mock://spotify"
    requests_mock.get(f"{spotify_url}/v1/me/tracks", text=content("get_library_tracks.json"))
    requests_mock.get(
        f"{spotify_url}/v1/albums?ids=54vbD17F1t5q3yHkj1cX37,0jvEFaPu8smfreB48YJBfB,4EUvdDfaYFFJtISsErAjuP",
        text=content("get_library_albums.json"))
    requests_mock.get(
        f"{spotify_url}/v1/artists?ids=64rxQRJsLgZwHHyWKB8fiF,5ENS85nZShljwNgg4wFD7D,5GiiOzSPyDaP5b4Bb7Moe2,10tYA1kHmiT7kCfF6HX0Wj",
        text=content("get_library_artists.json"))
    get_user_library = GetUserLibraryUseCase(SpotifyPort(spotify_url))
    assert (get_user_library.execute(spotify_user)[0].__dict__ ==
        {
            "uri": "spotify:track:2yAVzRiEQooPEJ9SYx11L3",
            "href": "https://api.spotify.com/v1/tracks/2yAVzRiEQooPEJ9SYx11L3",
            "name": "Blue (Da Ba Dee) - Gabry Ponte Ice Pop Radio",
            "isrc": "ITT019810102",
            "release_year": 2011,
            "album": "Europop",
            "language": "English",
            "artists": ["Eiffel 65", "Gabry Ponte"],
            "genres": ["bubblegum dance", "eurodance", "europop", "italian pop", "italo dance"]
        }
    )