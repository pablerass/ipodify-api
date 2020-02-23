# -*- coding: utf-8 -*-
from functools import wraps

from flask import request


from .ports import SpotifyNotAuthenticatedError


# TODO: Move this with SporityPort in a non called ports file
def spotify_auth(spotify_port):
    def caller(func):
        @wraps(func)
        def wrapper(*kargs, **kwargs):
            authorization = request.headers.get('Authorization')
            try:
                spotify_user = spotify_port.get_me(authorization)
            except SpotifyNotAuthenticatedError:
                return {"message": "Not authenticated or authorization"}, 401
            return func(spotify_user, *kargs, **kwargs)
        return wrapper
    return caller


def inject(*iargs, **ikwargs):
    def caller(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            nargs = args + iargs
            nkwargs = {**kwargs, **ikwargs}
            return func(*nargs, **nkwargs)
        return wrapper
    return caller
