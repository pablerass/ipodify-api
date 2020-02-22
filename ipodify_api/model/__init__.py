# -*- coding: utf-8 -*-

class Hasheable(object):
    @property
    def id(self):
        raise NotImplemented

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        return NotImplemented