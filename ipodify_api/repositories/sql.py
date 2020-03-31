# -*- coding: utf-8 -*-
"""This is crap for my autoenjoyment but does not seem to be really usefull in almost none real scenario."""
# TODO: Only allow to add Identifiable model

# TODO: Automatically import all mapped entities
from ..model.user import User               # noqa: F401
from ..model.playlist import Playlist       # noqa: F401

from sqlalchemy import create_engine, Column, String, ForeignKey
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class EntityMap():
    """Base class to map entities classes to SQL alchemy classes."""

    @classmethod
    def __get_entity_name(cls):
        class_name = cls.__name__
        if class_name.endswith('Map'):
            return class_name[:-(len('Map'))]

    @classmethod
    def get_entity(cls):
        """Get entity class."""
        return globals()[cls.__get_entity_name()]

    @staticmethod
    def __get_map_name(_class):
        return _class.__name__ + "Map"

    @staticmethod
    def get_map(_class):
        """Get map class."""
        return globals()[EntityMap.__get_map_name(_class)]

    def to_entity(self):
        """Conver map class to entity class."""
        d = {k: v for k, v in self.__dict__.items()
             if not k.startswith('_sa')}
        return self.get_entity()(**dict(d))


class UserMap(Base, EntityMap):
    """User entity map class."""

    __tablename__ = "users"

    name = Column(String, primary_key=True)


class PlaylistMap(Base, EntityMap):
    """Playlist entity map class."""

    __tablename__ = "playlists"

    name = Column(String, primary_key=True)
    owner = Column(String, ForeignKey('users.name'), primary_key=True)
    description = Column(String)


class SQLRepository(object):
    """Repository that stores model entities in SQL Alchemy managed database."""

    # TODO: Remove huge amount of duplicated code
    def __init__(self, connection_string=None):
        """Create SQL repository."""
        if connection_string is None:
            self.__engine = create_engine('sqlite:///:memory:')
            Base.metadata.create_all(self.__engine)
        else:
            self.__engine = create_engine(connection_string)
        self.__session = None

    @property
    def session(self):
        """Get SQL Alchemy repository session."""
        if self.__session is None:
            Session = sessionmaker(bind=self.__engine)
            self.__session = Session()

        return self.__session

    def _query(self, _class):
        return self.session.query(EntityMap.get_map(_class))

    def _key_columns(self, _class):
        return [c.name for c in EntityMap.get_map(_class).__table__.primary_key.columns.values()]

    def _id_filter(self, _class, _id):
        ids = _id.split(':')
        columns = self._key_columns(_class)
        return {column: ids[i] for i, column in enumerate(columns)}

    def add(self, entity):
        """Add entity to repository."""
        self.session.add(EntityMap.get_map(entity.__class__)(**entity.__dict__))

    def remove(self, entity):
        """Remove entity from repository."""
        self.remove_by_id(entity.__class__, entity.id)

    def remove_by_id(self, _class, _id):
        """Remove entity from repository by its class and id."""
        self._query(_class).filter_by(**self._id_filter(_class, _id)).delete()

    def remove_by_filter(self, _class, _filter):
        """Remove entities from repository by its class and a filter expression."""
        self._query(_class).filter_by(**_filter).delete()

    def contains(self, entity):
        """Return if the repository contains or not an entity."""
        return self.contains_by_id(entity.__class__, entity.id)

    def contains_by_id(self, _class, _id):
        """Return if the repository contains by its class and id."""
        count = self._query(_class).filter_by(**self._id_filter(_class, _id)).count()
        return count > 0

    def update(self, entity):
        """Update entity in repository.

        If the entity model object is updated its changes would not be persisted until it is updated in the repository
        itself. The repository stores a map of the entity, not the entity itself.
        """
        columns = self._key_columns(entity._class)
        entity_filter = {c: entity.getattr(c) for c in columns}
        entity_map = self.find_by_filter(**entity_filter).first()
        entity_map
        self.session.commit()

    def find_by_id(self, _class, _id):
        """Find entity in repository by its class and id."""
        entity_map = self._query(_class).filter_by(**self._id_filter(_class, _id)).first()
        return entity_map.to_entity()

    def find_by_filter(self, _class, _filter):
        """Find entitities in repository by its class and a filter expression."""
        entity_maps = self._query(_class).filter_by(**_filter).all()
        return [m.to_entity() for m in entity_maps]

    def list(self, _class):
        """List all repository entities of a specific class."""
        entity_maps = self._query(_class).all()
        return [m.to_entity() for m in entity_maps]

    def count(self, _class):
        """Count all repository entities of a specific class."""
        return self._query(_class).count()
