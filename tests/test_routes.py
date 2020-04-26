# -*- coding: utf-8 -*-
import pytest

import inject
from urllib.parse import urlparse

from secrets import token_urlsafe

from ipodify_api.app import create_app
from ipodify_api.gateways.spotify import SpotifyGateway, SpotifyUser
from ipodify_api.repositories.memory import MemoryRepository
from ipodify_api.use_cases import GetPlaylistsUseCase, AddPlaylistUseCase, GetPlaylistUseCase, RemovePlaylistUseCase


class MockSpotifyPort(object):
    def get_user(self, authotization):
        return SpotifyUser("hombredeincognito", token_urlsafe(32))


@pytest.fixture(scope="session")
def client():
    def test_config(binder):
        spotify_gateway = MockSpotifyPort()
        repository = MemoryRepository()
        binder.bind(SpotifyGateway, spotify_gateway)
        binder.bind(AddPlaylistUseCase, AddPlaylistUseCase(repository))
        binder.bind(GetPlaylistsUseCase, GetPlaylistsUseCase(repository))
        binder.bind(GetPlaylistUseCase, GetPlaylistUseCase(repository))
        binder.bind(RemovePlaylistUseCase, RemovePlaylistUseCase(repository))

    app = create_app(test_config)
    with app.test_client() as client:
       yield client


def test_not_found(client):
    response = client.get('/not_found')
    assert response.json['error'] == 404


def test_me(client):
    response = client.get('/me')
    assert response.json == {'id': 'hombredeincognito'}


def test_playlist(client):
    # TUNE: Here test are almost duplicating the ones defined in test_use_case.py
    playlist_invalid_dict = {
        "name": "a",
        "filter": {
            "$and": [
                {"$eq": {"album": "Veneno"}},
                {"$equ": {"release_year": 2010}}
            ]
        }
    }
    response = client.post('/playlists', json=playlist_invalid_dict)
    assert response.status_code == 400

    response = client.get('/playlists')
    assert response.status_code == 200
    assert response.json == {"playlists": []}

    playlist_dict = {
        "name": "a",
        "filter": {
            "$and": [
                {"$eq": {"album": "Veneno"}},
                {"$eq": {"release_year": 2010}}
            ]
        }
    }
    playlist_response_dict = dict(playlist_dict)
    playlist_response_dict.update({
        "visibility": "private",
        "owner": "hombredeincognito"
    })
    response = client.post('/playlists', json=playlist_dict)
    assert response.status_code == 201
    assert response.json == playlist_response_dict
    assert urlparse(response.headers['Location']).path == '/playlists/a'

    response = client.get('/playlists/a')
    assert response.status_code == 200
    assert response.json == playlist_response_dict

    response = client.get('/playlists/b')
    assert response.status_code == 404

    response = client.get('/playlists')
    assert response.status_code == 200
    assert response.json == {"playlists": [playlist_response_dict]}

    response = client.delete('/playlists/a')
    assert response.status_code == 200
    assert response.json == playlist_response_dict

    response = client.get('/playlists')
    assert response.status_code == 200
    assert response.json == {"playlists": []}