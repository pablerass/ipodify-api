# -*- coding: utf-8 -*-
"""Ipodify application."""
import inject

from flask import Flask

from json import JSONEncoder

from .ports.spotify import SpotifyPort
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


def create_app(inject_config=app_config):
    """Create app."""
    app = Flask(__name__)
    app.json_encoder = CustomJSONEncoder
    inject.configure(inject_config)

    with app.app_context():
        from . import routes

        app.register_blueprint(routes.main)

        return app
