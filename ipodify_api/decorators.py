# -*- coding: utf-8 -*-
import requests

from functools import wraps
from flask import request

from .model.user import RequestUser

from . import constants


def auth(func):
    @wraps(func)
    def wrapper():
        auth_header = {'Authorization': request.headers.get('Authorization')}
        me = f"{constants.SPOTIFY_API_URL}/v1/me"
        r = requests.get(me, headers=auth_header)
        if r.status_code == 401:
            return {"message": "Not authenticated or invalid auth token"}, 401
        r.raise_for_status()
        user_data = r.json()
        return func(RequestUser(user_data['id'], auth_header))
    return wrapper


def inject(*iargs, **ikwargs):
    def caller(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            nargs = args + iargs
            nkwargs = {**kwargs, **ikwargs}
            return func(*nargs, **nkwargs)
        return wrapper
    return caller
