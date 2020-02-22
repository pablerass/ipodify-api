# -*- coding: utf-8 -*-
from collections import defaultdict


# TODO: Move filter branch to Filterable entity class?
def filter_match(_filter, entity):
    for _property, value in _filter.items():
        if getattr(entity, _property) != value:
            return False

    return True


class MemoryRepository(object):
    def __init__(self):
        self.__repo = defaultdict(dict)

    def add(self, entity):
        self.__repo[entity.__class__][entity.id] = entity

    def remove(self, entity):
        del self.__repo[entity.__class__][entity.id]

    def remove_by_id(self, _class, _id):
        self.remove(self.find_by_id(_class, _id))

    def remove_by_filter(self, _class, _filter):
        for entity in self.find_by_filter(_class, _filter):
            self.remove(entity)

    def contains(self, entity):
        return self.contains_by_id(entity.__class__, entity.id)

    def contains_by_id(self, _class, _id):
        return _id in self.__repo[_class]

    def update(self, entity):
        self.add(entity)

    def find_by_id(self, _class, _id):
        return self.__repo[_class][_id]

    def find_by_filter(self, _class, _filter):
        return [entity for entity in self.__repo[_class].values()
                if filter_match(_filter, entity)]

    def list(self, _class):
        return self.__repo[_class]

    def count(self, _class):
        return len(self.__repo[_class])
