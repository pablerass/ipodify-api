# -*- coding: utf-8 -*-
import pytest

from ipodify_api.model.playlist import Playlist
from ipodify_api.model.user import User

from ipodify_api.repositories import MemoryRepo


def test_memory_repo():
    memory_repo = MemoryRepo()

    playlist = Playlist("a")
    memory_repo.add(playlist)
    assert memory_repo.contains(playlist)
    assert memory_repo.count(Playlist) == 1
    assert playlist == memory_repo.find_by_id(Playlist, "a")
    memory_repo.remove(playlist)
    assert not memory_repo.contains(playlist)
    assert not memory_repo.contains_by_id(Playlist, "a")
    memory_repo.add(Playlist("b"))
    assert memory_repo.count(Playlist) == 1
    memory_repo.remove_by_id(Playlist, "b")
    assert memory_repo.count(Playlist) == 0