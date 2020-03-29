# -*- coding: utf-8 -*-
import pytest

from ipodify_api.model.user import User
from ipodify_api.model.playlist import Playlist

from ipodify_api.repositories.memory import MemoryRepository, filter_match
from ipodify_api.repositories.sql import SQLRepository, EntityMap, UserMap, PlaylistMap


def test_filter_match():
    assert filter_match({"name": "a"}, User("a"))
    assert filter_match({"name": "a", "owner": User("b")}, Playlist("a", User("b")))


def test_entity_map():
    assert PlaylistMap.get_entity() == Playlist
    assert PlaylistMap.get_map(User) == UserMap


@pytest.mark.parametrize("repository", [MemoryRepository(), SQLRepository()])
def test_repository_with_simple_entity(repository):
    # TODO: Test find and remove when item does not exist
    user = User("a")
    repository.add(user)
    assert repository.contains(user)
    assert repository.count(User) == 1
    assert user == repository.find_by_id(User, "a")
    assert [user] == repository.find_by_filter(User, {"name": "a"})
    repository.remove(user)
    assert not repository.contains(user)
    assert not repository.contains_by_id(User, "a")
    repository.add(User("b"))
    assert repository.count(User) == 1
    repository.remove_by_id(User, "b")
    assert repository.count(User) == 0


#@pytest.mark.parametrize("repository", [MemoryRepository(), SQLRepository()])
@pytest.mark.parametrize("repository", [MemoryRepository()])
#@pytest.mark.parametrize("repository", [SQLRepository()])
def test_repository_with_composed_entity(repository):
    user = User("a")
    repository.add(user)
    playlist = Playlist("b", User("a"), "Some description")
    print(playlist)
    repository.add(playlist)
    playlist.description = "Other description"
    same_playlist = repository.find_by_id(Playlist, "a:b")
    print(same_playlist)
    repository.update(playlist)
    same_playlist = repository.find_by_id(Playlist, "a:b")
    print(same_playlist)
    #print(playlists_by_name)