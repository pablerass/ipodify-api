# -*- coding: utf-8 -*-

from ..model.user import User

from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class EntityMap():
    @classmethod
    def __get_entity_name(cls):
        class_name = cls.__name__
        if class_name.endswith('Map'):
            return class_name[:-(len('Map'))]

    @classmethod
    def get_entity(cls):
        return globals()[cls.__get_entity_name()]

    @staticmethod
    def __get_map_name(_class):
        return _class.__name__ + "Map"

    @staticmethod
    def get_map(_class):
        return globals()[EntityMap.__get_map_name(_class)]

    def to_entity(self):
        d = {k: v for k, v in self.__dict__.items()
             if not k.startswith('_sa')}
        return self.get_entity()(**dict(d))


class UserMap(Base, EntityMap):
    __tablename__ = "users"

    name = Column(String, primary_key=True)




class SQLRepository(object):
    # TODO: Remove huge amount of duplicated code
    def __init__(self, connection_string=None):
        if connection_string is None:
            self.__engine = create_engine('sqlite:///:memory:')
            Base.metadata.create_all(self.__engine)
        else:
            self.__engine = create_engine(connection_string)
        self.__session = None

    @property
    def session(self):
        if self.__session is None:
            Session = sessionmaker(bind=self.__engine)
            self.__session = Session()

        return self.__session

    def _query(self, _class):
        return self.session.query(EntityMap.get_map(_class))

    def _id_filter(self, _class, _id):
        ids = _id.split(':')
        columns = [c.name for c in EntityMap.get_map(_class).__table__.primary_key.columns.values()]
        return {column: ids[i] for i, column in enumerate(columns)}

    def add(self, entity):
        self.session.add(EntityMap.get_map(entity.__class__)(**entity.__dict__()))

    def remove(self, entity):
        self.remove_by_id(entity.__class__, entity.id)

    def remove_by_id(self, _class, _id):
        self._query(_class).filter_by(**self._id_filter(_class, _id)).delete()

    def remove_by_filter(self, _class, _filter):
        self._query(_class).filter_by(**_filter).delete()

    def contains(self, entity):
        return self.contains_by_id(entity.__class__, entity.id)

    def contains_by_id(self, _class, _id):
        count = self._query(_class).filter_by(**self._id_filter(_class, _id)).count()
        return count > 0

    # TODO: Implement update
    #def update(self, entity):
    #    self.add(entity)

    def find_by_id(self, _class, _id):
        entity_map = self._query(_class).filter_by(**self._id_filter(_class, _id)).first()
        return entity_map.to_entity()

    def find_by_filter(self, _class, _filter):
        entity_maps = self._query(_class).filter_by(**_filter).all()
        return [m.to_entity() for m in entity_maps]

    def list(self, _class):
        entity_maps = self._query(_class).all()
        return [m.to_entity() for m in entity_maps]

    def count(self, _class):
        return self._query(_class).count()
