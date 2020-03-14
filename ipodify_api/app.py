# -*- coding: utf-8 -*-
"""Ipodify application."""
import logging

from functools import partial
from flask import Flask, abort, jsonify, request
from json import JSONEncoder
from jsonschema import validate
from werkzeug.exceptions import HTTPException

from . import decorators
from .decorators import inject
from .ports import SpotifyPort
from .use_cases import GetUserLibraryUseCase, GetUserPlaylistsUseCase, AddPlaylistUseCase, GetPlaylistUseCase, \
                       RemovePlaylistUseCase
from .repositories.memory import MemoryRepository


class CustomJSONEncoder(JSONEncoder):
    """Ipodify application JSON Encoder."""

    def default(self, obj):
        """Get default JSON Encode value."""
        # TODO: Create JsonSerializable class to be used here
        if hasattr(obj, '__dict__'):
            return obj.__dict__()
        return obj


logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
app.json_encoder = CustomJSONEncoder

spotify_port = SpotifyPort()
repository = MemoryRepository()
auth = partial(decorators.spotify_auth(spotify_port))

get_user_playlists_uc = GetUserPlaylistsUseCase(repository)
get_user_library_uc = GetUserLibraryUseCase(spotify_port)
add_playlist_uc = AddPlaylistUseCase(repository)
get_playlist_uc = GetPlaylistUseCase(repository)
remove_playlist_uc = RemovePlaylistUseCase(repository)


@app.errorhandler(HTTPException)
def page_not_found(e):
    """404 error."""
    return jsonify(error=e.code, text=e.name), e.code

@app.route('/me', methods=['GET'])
@auth
def get_me(spotify_user):
    """Get library endpoint."""
    return {"id": spotify_user.name}


@app.route('/library', methods=['GET'])
@auth
@inject(get_user_library_uc)
def get_library(spotify_user, get_user_library_use_case):
    """Get library endpoint."""
    songs = get_user_library_use_case.execute(spotify_user)
    return {"songs": songs}


@app.route('/playlists', methods=['GET'])
@auth
@inject(get_user_playlists_uc)
def get_user_playlists(spotify_user, get_user_playlist_use_case):
    """Get playlists endpoint."""
    playlists = get_user_playlist_use_case.execute(spotify_user.name)
    return {
        'playlists': playlists
    }


@app.route('/playlists', methods=['POST'])
@auth
@inject(add_playlist_uc)
def add_playlist(spotify_user, add_playlist_use_case):
    """Add playlists endpoint."""
    request_content = request.json
    # TODO: Add json schema validation
    if request_content is None:
        abort(400)
    elif 'name' not in request_content:
        abort(422)
    name = request_content['name']
    playlist = add_playlist_use_case.execute(spotify_user.name, name)
    # TODO: Move this to a jsonable class
    return playlist.__dict__()


@app.route('/playlists/<name>', methods=['PUT'])
@auth
@inject(add_playlist_uc)
def set_playlist(spotify_user, add_playlist_use_case, name):
    """Set playlist endpoint."""
    print(add_playlist_uc)
    request_content = request.json
    # TODO: Add json schema validation
    if request_content is None:
        abort(400)
    # TODO: Add rename support
    elif 'name' in request_content and request_content['name'] != name:
        abort(422)
    # TODO: Try and catch error if user playlist with that name already exist
    playlist = add_playlist_use_case.execute(spotify_user.name, name)
    # TODO: Move this to a jsonable class
    return playlist.__dict__()


@app.route('/playlists/<name>', methods=['GET'])
@auth
@inject(get_playlist_uc)
def get_playlist(spotify_user, get_playlist_use_case, name):
    """Add playlist endpoint."""
    playlist = get_playlist_use_case.execute(spotify_user.name, name)
    if not playlist:
        abort(404)
    # TODO: Move this to a jsonable class
    return playlist.__dict__()


@app.route('/playlists/<name>', methods=['DELETE'])
@auth
@inject(remove_playlist_uc)
def remove_playlist(spotify_user, remove_playlist_use_case, name):
    """Remove playlist endpoint."""
    if not remove_playlist_use_case.execute(spotify_user.name, name):
        abort(404)
    return ""
