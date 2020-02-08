# -*- coding: utf-8 -*-
from collections import defaultdict


class MemoryRepo(object):
    def __init__(self):
        self.__repo = defaultdict(dict)

    def add(self, entity):
        self.__repo[entity.__class__][entity.id] = entity

    def remove(self, entity):
        del self.__repo[entity.__class__][entity.id]

    def remove_by_id(self, _class, _id):
        self.remove(self.find_by_id(_class, _id))

    def remove_by_filter(self, _class, _filter):
        for entity in self.find(_class, _filter):
            self.remove(entity.id)

    def contains(self, entity):
        return self.contains_by_id(entity.__class__, entity.id)

    def contains_by_id(self, _class, _id):
        return _id in self.__repo[_class]

    def update(self, entity):
        self.add(entity)

    def find_by_id(self, _class, _id):
        return self.__repo[_class][_id]

    def find_by_filter(self, _class, _filter):
        pass

    def count(self, _class):
        return len(self.__repo[_class])
