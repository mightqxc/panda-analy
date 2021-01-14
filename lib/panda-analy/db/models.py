"""
SQLAlchemy models
"""

import datetime
from sqlalchemy import Table,Enum,Index
from sqlalchemy import BigInteger, Boolean, Column, DateTime, Float, Integer, SmallInteger, String as _String, Text
from sqlalchemy.orm import object_mapper
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declared_attr
from db.constants import JobState

Base = declarative_base()

class ModelBase(object):
    """Base class of Models"""

    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)

    @declared_attr
    def created_at(cls):  # pylint: disable=no-self-argument
        return Column("created_at", DateTime, default=datetime.datetime.utcnow)

    @declared_attr
    def updated_at(cls):  # pylint: disable=no-self-argument
        return Column("updated_at", DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def save(self, flush=True, session=None):
        """Save this object"""
        session.add(self)
        if flush:
            session.flush()

    def delete(self, flush=True, session=None):
        """Delete this object"""
        session.delete(self)
        if flush:
            session.flush()

    def update(self, values, flush=True, session=None):
        """dict.update() behaviour"""
        for k, v in values.iteritems():
            self[k] = v
        self["updated_at"] = datetime.datetime.utcnow()
        if session and flush:
            session.flush()

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def __iter__(self):
        self._i = iter(object_mapper(self).columns)
        return self

    def next(self):
        n = self._i.next().name
        return n, getattr(self, n)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def to_dict(self):
        return {key: value for key, value
                in self.__dict__.items() if not key.startswith('_')}

    def to_dict_json(self):
        return {key: self._expand_item(value) for key, value
                in self.__dict__.items() if not key.startswith('_')}



class Pandajob(ModelBase, Base):
    __tablename__ = 'PandaJob'
    panda_id = Column(Integer(),primary_key=True)
    job_state = Column(Enum(JobState),index=True)
    error_code = Column(String(64))
    error_message = Column(Text())
    inputfilebyte = Column(BigInteger)
    endtime = Column(DateTime,index=True)
    checksum_adler = Column(String(8))
    duration_time = Column(Float())
    retry_count = Column(SmallInteger, server_default='0')
    timestamp = Column(DateTime,index=True)

class TestTable(ModelBase, Base):
    __tablename__ = 'TestTable'
    test_id = Column(Integer(),primary_key=True)


def register_models(engine):
    """
    Creates database tables for all models with the given engine
    """

    models = (Pandajob, TestTable)

    for model in models:
        model.metadata.create_all(engine)


def unregister_models(engine):
    """
    Drops database tables for all models with the given engine
    """

    models = (Pandajob, TestTable)

    for model in models:
        model.metadata.drop_all(engine)
