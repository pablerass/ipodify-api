# -*- coding: utf-8 -*-
import requests

from flask import request

from .model.user import RequestUser

from . import constants


def auth(func):
    def wrapper():
        auth_header = {'Authorization': request.headers.get('Authorization')}
        me = f"{constants.SPOTIFY_API_URL}/v1/me"
        r = requests.get(me, headers=auth_header)
        r.raise_for_status()
        # TODO: Return error when error
        user_data = r.json()
        return func(RequestUser(user_data['id'], auth_header))

    # Renaming the function name to solve issues with flask
    wrapper.__name__ = func.__name__
    return wrapper
