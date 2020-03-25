# -*- coding: utf-8 -*-


from . import Hasheable


class User(Hasheable):
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    @property
    def __dict__(self):
        return {
            'name': self.__name,
        }

    def __repr__(self):
        return str(self.__dict__)

    @property
    def id(self):
        return self.__name
