# -*- coding: utf-8 -*-
import pytest

import inject
import json

from secrets import token_urlsafe

from ipodify_api.app import create_app
from ipodify_api.ports.spotify import SpotifyPort, SpotifyUser


class MockSpotifyPort(object):
    def get_user(self, authotization):
        return SpotifyUser("hombredeincognito", token_urlsafe(32))


@pytest.fixture(scope="session")
def client():
    def config(binder):
        binder.bind(SpotifyPort, MockSpotifyPort())

    app = create_app(config)
    with app.test_client() as client:
       yield client


def test_not_found(client):
    response = client.get('/not_found')
    assert json.loads(response.data)['error'] == 404


def test_me(client):
    response = client.get('/me')
    assert json.loads(response.data) == {'id': 'hombredeincognito'}