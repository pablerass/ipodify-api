# -*- coding: utf-8 -*-
import logging

from flask import Flask, abort, jsonify
from json import JSONEncoder
from werkzeug.exceptions import HTTPException

from .decorators import auth, inject
from .model import BaseModel
from .model.playlist import Playlist
from .use_cases import GetLibraryUseCase, GetPlaylistsUseCase, AddPlaylistUseCase, RemovePlaylistUseCase
from .repositories import MemoryRepository


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BaseModel):
            return obj.__dict__()
        return obj

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
app.json_encoder = CustomJSONEncoder

repository = MemoryRepository()
add_playlist_uc = AddPlaylistUseCase(repository)
remove_playlist_uc = RemovePlaylistUseCase(repository)
get_playlists_uc = GetPlaylistsUseCase(repository)
get_library_uc = GetLibraryUseCase()


@app.errorhandler(HTTPException)
def page_not_found(e):
    return jsonify(error=e.code, text=e.name), e.code


@app.route('/library', methods=['GET'])
@auth
@inject(get_library_uc)
def get_library(user, get_library_use_case):
    return get_library_use_case.execute(user)


@app.route('/playlists', methods=['GET'])
@auth
@inject(get_playlists_uc)
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


@app.route('/playlists/<name>', methods=['DELETE'])
@auth
@inject(remove_playlist_uc)
def remove_playlists(user, remove_playlist_use_case, name):
    if not remove_playlist_use_case.execute(user.name, Playlist(name)):
        abort(404)
    return ""
