# -*- coding: utf-8 -*-
import pytest

from ipodify_api.model.user import UserCollection
from ipodify_api.model.playlist import Playlist

from ipodify_api.use_cases import AddPlaylistUseCase, GetPlaylistsUseCase, RemovePlaylistUseCase

@pytest.fixture
def user_collection():
    return UserCollection()

def test_playlist_use_cases(user_collection):
    add_playlist = AddPlaylistUseCase(user_collection)
    get_playlists = GetPlaylistsUseCase(user_collection)
    remove_playlist = RemovePlaylistUseCase(user_collection)

    user_name = "a"
    playlist = Playlist("a")
    add_playlist.execute(user_name, playlist)
    assert get_playlists.execute(user_name) == set([playlist])
    remove_playlist.execute(user_name, playlist)
    assert get_playlists.execute(user_name) == set()