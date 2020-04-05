# -*- coding: utf-8 -*-
"""Ipodify application."""
import inject
import logging

from functools import partial
from flask import Flask, abort, jsonify, request

from json import JSONEncoder
from werkzeug.exceptions import HTTPException

from .ports.spotify import SpotifyPort, spotify_auth
from .use_cases import GetUserTrackLibraryUseCase, GetPlaylistsUseCase, AddPlaylistUseCase, GetPlaylistUseCase, \
                       RemovePlaylistUseCase
from .repositories.memory import MemoryRepository


class CustomJSONEncoder(JSONEncoder):
    """Ipodify application JSON Encoder."""

    def default(self, obj):
        """Get default JSON Encode value."""
        # TODO: Create JsonSerializable class to be used here
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        return obj


logging.basicConfig(level=logging.DEBUG)


def app_config(binder):
    """Configure app inject bindings."""
    spotify_port = SpotifyPort()
    repository = MemoryRepository()

    binder.bind(SpotifyPort, spotify_port)
    binder.bind(GetUserTrackLibraryUseCase, GetUserTrackLibraryUseCase(spotify_port))
    binder.bind(GetPlaylistsUseCase, GetPlaylistsUseCase(repository))
    binder.bind(GetPlaylistUseCase, GetPlaylistUseCase(repository))
    binder.bind(AddPlaylistUseCase, AddPlaylistUseCase(repository))
    binder.bind(RemovePlaylistUseCase, RemovePlaylistUseCase(repository))


def create_app(inject_config):
    """Create app."""
    app = Flask(__name__)
    app.json_encoder = CustomJSONEncoder
    inject.configure(inject_config)
    return app


app = create_app(app_config)


auth = partial(spotify_auth(inject.instance(SpotifyPort)))


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
@inject.params(get_user_track_library_use_case=GetUserTrackLibraryUseCase)
def get_library(spotify_user, get_user_track_library_use_case):
    """Get library endpoint."""
    songs = get_user_track_library_use_case.execute(spotify_user)
    return {"songs": songs}


@app.route('/playlists', methods=['GET'])
@auth
@inject.params(get_playlists_use_case=GetPlaylistsUseCase)
def get_playlists(spotify_user, get_playlists_use_case):
    """Get playlists endpoint."""
    playlists = get_playlists_use_case.execute(spotify_user.name)
    return {
        'playlists': playlists
    }


@app.route('/playlists', methods=['POST'])
@auth
@inject.params(add_playlist_use_case=AddPlaylistUseCase)
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
    return playlist.__dict__


@app.route('/playlists/<name>', methods=['PUT'])
@auth
@inject.params(add_playlist_use_case=AddPlaylistUseCase)
def set_playlist(spotify_user, add_playlist_use_case, name):
    """Set playlist endpoint."""
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
    return playlist.__dict__


@app.route('/playlists/<name>', methods=['GET'])
@auth
@inject.params(get_playlist_use_case=GetPlaylistUseCase)
def get_playlist(spotify_user, get_playlist_use_case, name):
    """Add playlist endpoint."""
    playlist = get_playlist_use_case.execute(spotify_user.name, name)
    if not playlist:
        abort(404)
    # TODO: Move this to a jsonable class
    return playlist.__dict__


@app.route('/playlists/<name>', methods=['DELETE'])
@auth
@inject.params(remove_playlist_use_case=RemovePlaylistUseCase)
def remove_playlist(spotify_user, remove_playlist_use_case, name):
    """Remove playlist endpoint."""
    if not remove_playlist_use_case.execute(spotify_user.name, name):
        abort(404)
    return ""
