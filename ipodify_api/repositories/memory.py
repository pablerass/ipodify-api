# -*- coding: utf-8 -*-
"""Simple in memory model entities repository."""
from collections import defaultdict
from inspect import signature

# TODO: Only allow to add Identifiable model

# TODO: Move filter branch to Filterable entity class?
def filter_match(_filter, entity):
    """Check if an entity match against a filter expression."""
    for _property, value in _filter.items():
        if getattr(entity, _property) != value:
            return False

    return True


class MemoryRepository(object):
    """Repository that stores model entities in memory."""

    def __init__(self):
        """Create memory repository."""
        self.__repo = defaultdict(dict)

    def add(self, *entities):
        """Add entities to repository."""
        for entity in entities:
            arguments = signature(entity.__init__).parameters.keys()
            arguments_dict = {a: getattr(entity, a) for a in arguments}
            cloned_entity = entity.__class__(**arguments_dict)
            self.__repo[entity.__class__][entity.id] = cloned_entity

    def remove(self, *entities):
        """Remove entities from repository."""
        for entity in entities:
            del self.__repo[entity.__class__][entity.id]

    def remove_by_id(self, _class, _id):
        """Remove entity from repository by its class and id."""
        self.remove(self.find_by_id(_class, _id))

    def remove_by_filter(self, _class, _filter):
        """Remove entities from repository by its class and a filter expression."""
        for entity in self.find_by_filter(_class, _filter):
            self.remove(entity)

    def contains(self, entity):
        """Return if the repository contains or not an entity."""
        return self.contains_by_id(entity.__class__, entity.id)

    def contains_by_id(self, _class, _id):
        """Return if the repository contains by its class and id."""
        return _id in self.__repo[_class]

    def update(self, *entities):
        """Update repository entity.

        If the entity model object is updated its changes would not be persisted until it is updated in the repository
        itself. The repository stores a copy of the entity, not the entity itself.
        """
        self.add(*entities)

    def find_by_id(self, _class, _id):
        """Find entity in repository by its class and id."""
        return self.__repo[_class][_id]

    def find_by_filter(self, _class, _filter):
        """Find entitities in repository by its class and a filter expression."""
        return [entity for entity in self.__repo[_class].values()
                if filter_match(_filter, entity)]

    def list(self, _class):
        """List all repository entities of a specific class."""
        return self.__repo[_class]

    def count(self, _class):
        """Count all repository entities of a specific class."""
        return len(self.__repo[_class])
