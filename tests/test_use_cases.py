# -*- coding: utf-8 -*-
import pytest

from ipodify_api.model.playlist import Playlist
from ipodify_api.model.user import User

from ipodify_api.repositories.memory import MemoryRepository, filter_match

from ipodify_api.use_cases import AddPlaylistUseCase, GetUserPlaylistsUseCase, RemovePlaylistUseCase


@pytest.fixture
def repository():
    return MemoryRepository()


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