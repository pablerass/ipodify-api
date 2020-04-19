# -*- coding: utf-8 -*-
"""Ipodify api routes."""
import inject

from functools import partial
from flask import Blueprint, abort, request

from .gateways.spotify import SpotifyPort, spotify_auth
from .schemas import body_schema
from .use_cases import GetFilterPreviewUseCase, GetLibraryUseCase, GetPlaylistsUseCase, AddPlaylistUseCase, \
                       GetPlaylistUseCase, RemovePlaylistUseCase


api = Blueprint('api', __name__)
auth = partial(spotify_auth(inject.instance(SpotifyPort)))


@api.route('/me', methods=['GET'])
@auth
def get_me(spotify_user):
    """Get library endpoint."""
    return {"id": spotify_user.name}


@api.route('/library', methods=['GET'])
@auth
@inject.params(get_library_use_case=GetLibraryUseCase)
def get_library(spotify_user, get_library_use_case):
    """Get library endpoint."""
    tracks = get_library_use_case.execute(spotify_user)
    return {"tracks": tracks}


@api.route('/filter_preview', methods=['GET'])
@body_schema("filter")
@auth
@inject.params(get_filter_preview_use_case=GetFilterPreviewUseCase)
def get_filter_preview(spotify_user, get_filter_preview_use_case):
    """Get filter preview endpoint."""
    filter_dict = request.json
    tracks = GetFilterPreviewUseCase.execute(spotify_user, filter_dict)
    return {
        "filter": filter_dict,
        "tracks": tracks
    }


@api.route('/playlists', methods=['GET'])
@auth
@inject.params(get_playlists_use_case=GetPlaylistsUseCase)
def get_playlists(spotify_user, get_playlists_use_case):
    """Get playlists endpoint."""
    playlists = get_playlists_use_case.execute(spotify_user.name)
    return {
        'playlists': playlists
    }


@api.route('/playlists', methods=['POST'])
@body_schema("playlist")
@auth
@inject.params(add_playlist_use_case=AddPlaylistUseCase)
def add_playlist(spotify_user, add_playlist_use_case):
    """Add playlists endpoint."""
    request_content = request.json
    playlist = add_playlist_use_case.execute(request_content['name'], spotify_user.name, request_content['filter'])
    # TODO: Move this to a jsonable class
    return playlist.__dict__


@api.route('/playlists/<name>', methods=['PUT'])
@body_schema("playlist")
@auth
@inject.params(add_playlist_use_case=AddPlaylistUseCase)
def set_playlist(spotify_user, add_playlist_use_case, name):
    """Set playlist endpoint."""
    request_content = request.json
    if request_content is None:
        abort(400)
    # TODO: Add rename support
    elif 'name' in request_content and request_content['name'] != name:
        abort(422)
    # TODO: Try and catch error if user playlist with that name already exist
    playlist = add_playlist_use_case.execute(spotify_user.name, name)
    # TODO: Move this to a jsonable class
    return playlist.__dict__


@api.route('/playlists/<name>', methods=['GET'])
@auth
@inject.params(get_playlist_use_case=GetPlaylistUseCase)
def get_playlist(spotify_user, get_playlist_use_case, name):
    """Add playlist endpoint."""
    playlist = get_playlist_use_case.execute(spotify_user.name, name)
    if not playlist:
        abort(404)
    # TODO: Move this to a jsonable class
    return playlist.__dict__


@api.route('/playlists/<name>', methods=['DELETE'])
@auth
@inject.params(remove_playlist_use_case=RemovePlaylistUseCase)
def remove_playlist(spotify_user, remove_playlist_use_case, name):
    """Remove playlist endpoint."""
    if not remove_playlist_use_case.execute(spotify_user.name, name):
        abort(404)
    return ""
