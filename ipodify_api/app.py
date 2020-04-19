# -*- coding: utf-8 -*-
"""Ipodify application."""
import inject

from json import JSONEncoder
from flask import Flask
from werkzeug.exceptions import HTTPException

from .error import handle_http_exception
from .gateways.spotify import SpotifyGateway
from .repositories.memory import MemoryRepository
from .use_cases import GetFilterPreviewUseCase, GetLibraryUseCase, GetPlaylistsUseCase, \
                       AddPlaylistUseCase, GetPlaylistUseCase, RemovePlaylistUseCase


class CustomJSONEncoder(JSONEncoder):
    """Ipodify application JSON Encoder."""

    def default(self, obj):
        """Get default JSON Encode value."""
        # TODO: Create JsonSerializable class to be used here
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        return obj


def app_config(binder):
    """Configure app inject bindings."""
    spotify_gateway = SpotifyGateway()
    repository = MemoryRepository()
    get_library_use_case = GetLibraryUseCase(spotify_gateway)

    binder.bind(SpotifyGateway, spotify_gateway)
    binder.bind(GetLibraryUseCase, get_library_use_case)
    binder.bind(GetFilterPreviewUseCase, GetFilterPreviewUseCase(spotify_gateway))
    binder.bind(GetPlaylistsUseCase, GetPlaylistsUseCase(repository))
    binder.bind(GetPlaylistUseCase, GetPlaylistUseCase(repository))
    binder.bind(AddPlaylistUseCase, AddPlaylistUseCase(repository))
    binder.bind(RemovePlaylistUseCase, RemovePlaylistUseCase(repository))


def create_app(inject_config=app_config):
    """Create app."""
    app = Flask(__name__)
    app.json_encoder = CustomJSONEncoder
    inject.configure(inject_config)

    with app.app_context():
        from . import routes

        app.register_error_handler(HTTPException, handle_http_exception)
        app.register_blueprint(routes.api)

        return app
