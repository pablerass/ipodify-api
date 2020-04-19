# -*- coding: utf-8 -*-
import pytest

import inject

from secrets import token_urlsafe

from ipodify_api.app import create_app
from ipodify_api.gateways.spotify import SpotifyGateway, SpotifyUser
from ipodify_api.repositories.memory import MemoryRepository
from ipodify_api.use_cases import AddPlaylistUseCase


class MockSpotifyPort(object):
    def get_user(self, authotization):
        return SpotifyUser("hombredeincognito", token_urlsafe(32))


@pytest.fixture(scope="session")
def client():
    def config(binder):
        spotify_gateway = MockSpotifyPort()
        repository = MemoryRepository()
        binder.bind(SpotifyGateway, spotify_gateway)
        binder.bind(AddPlaylistUseCase, AddPlaylistUseCase(repository))

    app = create_app(config)
    with app.test_client() as client:
       yield client


def test_not_found(client):
    response = client.get('/not_found')
    assert response.json['error'] == 404


def test_me(client):
    response = client.get('/me')
    assert response.json == {'id': 'hombredeincognito'}


def test_post_playlist(client):
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
    assert response.json['error'] == 400

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
    assert response.json == playlist_response_dict