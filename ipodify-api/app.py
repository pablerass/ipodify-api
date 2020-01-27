# -*- coding: utf-8 -*-
import logging

from flask import Flask

from .decorators import auth
from .model.user import UserCollection
from .model.playlist import Playlist
from .use_cases import GetLibraryUseCase, GetPlaylistsUseCase, AddPlaylistUseCase

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

user_collection = UserCollection()

@app.route('/library', methods=['GET'])
@auth
def get_library(user):
    return GetLibraryUseCase().execute(user)

@app.route('/playlists', methods=['GET'])
@auth
def get_playlists(user):
    playlists = GetPlaylistsUseCase(user_collection).execute(user.name)
    print(playlists)
    return {
        'playlists': []
    }

@app.route('/playlists', methods=['POST'])
@auth
def add_playlists(user):
    AddPlaylistUseCase(user_collection).execute(user.name, Playlist("aaaa"))
    return ""


@app.route('/nothing', methods=['GET'])
@auth
def nothing(user):
    return user.name
