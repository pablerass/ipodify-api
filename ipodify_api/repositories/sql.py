# -*- coding: utf-8 -*-

from ..model.user import User

from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserMap(Base):
    __tablename__ = "users"

    name = Column(String, primary_key=True)

    def to_entity(self):
        d = {k: v for k, v in self.__dict__.items()
             if not k.startswith('_sa')}
        return User(**dict(d))


# TODO: Manage this map in a better way, self generate, maybe?
CLASS_MAP = {
    User: UserMap
}


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

    def add(self, entity):
        self.session.add(CLASS_MAP[entity.__class__](**entity.__dict__()))

    def remove(self, entity):
        self.remove_by_id(entity.__class__, entity.id)

    def remove_by_id(self, _class, _id):
        map_class = CLASS_MAP[_class]
        id_column_name = map_class.__table__.primary_key.columns.values()[0].name
        self.session.query(map_class).filter_by(**{id_column_name: _id}).delete()

    def remove_by_filter(self, _class, _filter):
        map_class = CLASS_MAP[_class]
        self.session.query(map_class).filter_by(**_filter).delete()

    def contains(self, entity):
        return self.contains_by_id(entity.__class__, entity.id)

    def contains_by_id(self, _class, _id):
        map_class = CLASS_MAP[_class]
        id_column_name = map_class.__table__.primary_key.columns.values()[0].name
        count = self.session.query(map_class).filter_by(**{id_column_name: _id}).count()
        return count > 0

    # TODO: Implement update
    #def update(self, entity):
    #    self.add(entity)

    def find_by_id(self, _class, _id):
        # TODO: Enjoy how this explode with multiple primar key columns
        map_class = CLASS_MAP[_class]
        id_column_name = map_class.__table__.primary_key.columns.values()[0].name
        entity_map = self.session.query(map_class).filter_by(**{id_column_name: _id}).first()
        return entity_map.to_entity()

    def find_by_filter(self, _class, _filter):
        map_class = CLASS_MAP[_class]
        entity_maps = self.session.query(map_class).filter_by(**_filter).all()
        return [m.to_entity() for m in entity_maps]

    def list(self, _class):
        map_class = CLASS_MAP[_class]
        entity_maps = self.session.query(map_class).all()
        return [m.to_entity() for m in entity_maps]

    def count(self, _class):
        map_class = CLASS_MAP[_class]
        return self.session.query(map_class).count()
