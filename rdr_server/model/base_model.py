"""Defines the declarative base. Import this and extend from Base for all rdr
tables. Extend MetricsBase for all metrics tables."""

import json

from dateutil.tz import tzutc
from sqlalchemy import MetaData, Column, BigInteger, text
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import TypeDecorator


# Do not use the cls=xxxx parameter, create a mixin class and add them directly
# to the models.
BaseModel = declarative_base(metadata=MetaData(schema='rdrv2'))

# MetricsBase is the parent for all models in the "metrics" DB. These are
# collected separately for DB migration purposes.
BaseMetricsModel = declarative_base(metadata=MetaData(schema='metricsv2'))


class UTCDateTime(TypeDecorator):
    """
    Force timestamps to UTC
    """
    impl = DATETIME(fsp=6)

    def process_bind_param(self, value, engine):
        # pylint: disable=unused-argument
        if value is not None and value.tzinfo:
            return value.astimezone(tzutc()).replace(tzinfo=None)
        return value


class ModelMixin(object):
    """
    Base Mixin for all models. Includes methods for importing/exporting JSON data.
    """

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    pkId = Column('id', BigInteger, primary_key=True, autoincrement=True)
    created = Column('created', DATETIME(fsp=6), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    modified = Column('modified', DATETIME(fsp=6), nullable=False,
                      server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
                      )

    def from_json(self, *args, **kwargs):
        """
        If parameter values in args, then the value is expected to be a dictionary from a json response
        from the server.

        If parameter values are in kwargs, then they are named parameters passed when the object is instantiated.

        # TODO: This method needs work to fit with sqlachemey, may need return a new clean object.

        """
        if args is not None and len(args) is not 0 and args[0] is not None:
            for key, value in args[0].items():
                self.__dict__[key] = value
                # print('{0} : {1}'.format(key, value))

        else:
            for key, value in kwargs.items():
                self.__dict__[key] = value
                # print('{0} : {1}'.format(key, value))

    def to_json(self):
        """
        Dump class to json string
        :return: json string
        """
        data = self.__dict__.copy()
        for key in self.__dict__:
            if key.startswith('_'):
                data.pop(key)

        return json.dumps(data, default=lambda o: o.__dict__, sort_keys=True, indent=2)

    def to_dict(self):
        """
        Dump class to python dict
        :return: dict
        """
        data = dict()
        for key, value in self.__dict__.items():
            if not key.startswith("_") and value is not None:
                data[key] = value
        return data

    def dict_to_obj_array(self, cls, data):
        """
        Convert dict to array of objects of type cls
        """
        if data is None:
            return None

        ol = list()
        for x in range(0, len(data)):
            ol.append(cls(data[x]))

        return ol

    def __repr__(self):
        return self.to_json()


def get_column_name(model_type, field_name):
    return getattr(model_type, field_name).property.columns[0].name
