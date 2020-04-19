# -*- coding: utf-8 -*-
import pytest

from secrets import token_urlsafe

from ipodify_api.gateways.spotify import SpotifyGateway, SpotifyUser


@pytest.fixture(scope="session")
def spotify_gateway():
    return SpotifyGateway("http://mockspotify")


def test_get_user(spotify_gateway, requests_mock):
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
    requests_mock.get(f"{spotify_gateway.url}/v1/me", json=me)
    auth_token = token_urlsafe(32)
    assert spotify_gateway.get_user(auth_token) == SpotifyUser("hombredeincognito", auth_token)