# -*- coding: utf-8 -*-
import logging

from flask import Flask

from .decorators import auth, inject
from .model.user import UserCollection
from .model.playlist import Playlist
from .use_cases import GetLibraryUseCase, GetPlaylistsUseCase, AddPlaylistUseCase

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

user_collection = UserCollection()
add_playlist_uc = AddPlaylistUseCase(user_collection)
get_playlist_uc = GetPlaylistsUseCase(user_collection)
get_library_uc = GetLibraryUseCase()


@app.route('/library', methods=['GET'])
@auth
@inject(get_library_uc)
def get_library(user, get_library_use_case):
    return get_library_use_case.execute(user)


@app.route('/playlists', methods=['GET'])
@auth
@inject(get_playlist_uc)
def get_playlists(user, get_playlist_use_case):
    playlists = get_playlist_use_case.execute(user.name)
    return {
        'playlists': playlists
    }


@app.route('/playlists', methods=['POST'])
@auth
@inject(add_playlist_uc)
def add_playlists(user, add_playlist_use_case):
    add_playlist_use_case.execute(user.name, Playlist("aaaa"))
    return ""
