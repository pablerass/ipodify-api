# -*- coding: utf-8 -*-


from . import Hasheable


class RequestUser(object):
    def __init__(self, name, auth_header):
        self.__name = name
        self.__auth_header = auth_header

    @property
    def name(self):
        return self.__name

    @property
    def auth_header(self):
        return self.__auth_header


class User(Hasheable):
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    def __dict__(self):
        return {
            'name': self.__name,
        }

    def __repr__(self):
        return str(self.__dict__())

    @property
    def id(self):
        return self.__name
