# -*- coding: utf-8 -*-
import pytest

import json

from ipodify_api.app import app


# TODO: Modify app to allow mock and fake ports
@pytest.fixture
def client():
    with app.test_client() as client:
       yield client

def test_me(client, requests_mock):
    me = {
        "display_name": "hombredeincognito",
        "external_urls": {
            "spotify": "https://open.spotify.com/user/hombredeincognito"
        },
        "followers": {
            "href": None,
            "total": 0
        },
        "href": "https://api.spotify.com/v1/users/hombredeincognito",
        "id": "hombredeincognito",
        "images": [],
        "type": "user",
        "uri": "spotify:user:hombredeincognito"
    }
    requests_mock.get('https://api.spotify.com/v1/me', json=me)
    response = client.get('/me')
    assert json.loads(response.data) == {'id': 'hombredeincognito'}