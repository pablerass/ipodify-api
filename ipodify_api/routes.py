# -*- coding: utf-8 -*-
"""Ipodify main routes."""
import inject

from functools import partial
from flask import Blueprint, abort, request

from .ports.spotify import SpotifyPort, spotify_auth
from .use_cases import GetUserTrackLibraryUseCase, GetPlaylistsUseCase, AddPlaylistUseCase, GetPlaylistUseCase, \
                       RemovePlaylistUseCase


main = Blueprint('main', __name__)
auth = partial(spotify_auth(inject.instance(SpotifyPort)))


@main.route('/me', methods=['GET'])
@auth
def get_me(spotify_user):
    """Get library endpoint."""
    return {"id": spotify_user.name}


@main.route('/library', methods=['GET'])
@auth
@inject.params(get_user_track_library_use_case=GetUserTrackLibraryUseCase)
def get_library(spotify_user, get_user_track_library_use_case):
    """Get library endpoint."""
    songs = get_user_track_library_use_case.execute(spotify_user)
    return {"songs": songs}


@main.route('/playlists', methods=['GET'])
@auth
@inject.params(get_playlists_use_case=GetPlaylistsUseCase)
def get_playlists(spotify_user, get_playlists_use_case):
    """Get playlists endpoint."""
    playlists = get_playlists_use_case.execute(spotify_user.name)
    return {
        'playlists': playlists
    }


@main.route('/playlists', methods=['POST'])
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


@main.route('/playlists/<name>', methods=['PUT'])
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


@main.route('/playlists/<name>', methods=['GET'])
@auth
@inject.params(get_playlist_use_case=GetPlaylistUseCase)
def get_playlist(spotify_user, get_playlist_use_case, name):
    """Add playlist endpoint."""
    playlist = get_playlist_use_case.execute(spotify_user.name, name)
    if not playlist:
        abort(404)
    # TODO: Move this to a jsonable class
    return playlist.__dict__


@main.route('/playlists/<name>', methods=['DELETE'])
@auth
@inject.params(remove_playlist_use_case=RemovePlaylistUseCase)
def remove_playlist(spotify_user, remove_playlist_use_case, name):
    """Remove playlist endpoint."""
    if not remove_playlist_use_case.execute(spotify_user.name, name):
        abort(404)
    return ""
