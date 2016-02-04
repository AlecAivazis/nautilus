# third party imports
from sqlalchemy.ext.declarative import declared_attr
from flask.ext.jsontools import JsonSerializableBase
from sqlalchemy.ext.declarative import declarative_base

# local imports
from .typeDecorators import *
from .mixins import *

from ...ext import db as internal_db
from ...ext import admin as internal_admin

class Meta(type):
    """
        The base metaclass for the nautilus models. Currently, it's primary use is to
        automatically register a model class with the internal_admin after it is created.
    """

    def __init__(self, name, bases, attributes, **kwds):
        # create the super class
        super().__init__(name, bases, attributes, **kwds)
        # if the class is not a nautilus base class
        if 'nautilus_base' not in attributes or not attributes['nautilus_base']:
            # perform the necessary functions
            self.onCreation()

        return

class MixedMeta(Meta, type(internal_db.Model)):
    """
        This meta class mixes the sqlalchemy model meta class and the nautilus one.
    """


JsonBase = declarative_base(cls=(JsonSerializableBase,))

class BaseModel(internal_db.Model, JsonBase, metaclass=MixedMeta):

    nautilus_base = True # necessary to prevent meta class behavior on this model

    def __init__(self, **kwargs):
        """ treat kwargs as attribute assignment """
        # loop over the given kwargs
        for key, value in kwargs.items():
            # treat them like attribute assignments
            setattr(self, key, value)

    @classmethod
    def onCreation(cls):
        # register the class with the internal_admin interface
        internal_admin.add_model(cls)


    def save(self):
        # add the entry to the internal_db session
        internal_db.session.add(self)
        # commit the entry
        internal_db.session.commit()

    @declared_attr
    def __tablename__(self):
        return '{}_{}'.format(self.__module__.split('.')[-1], self.__name__.lower())

    __abstract__ = True
    __table_args__ = dict(mysql_charset='utf8')


