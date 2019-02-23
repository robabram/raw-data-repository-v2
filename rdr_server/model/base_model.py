"""Defines the declarative base. Import this and extend from Base for all rdr
tables. Extend MetricsBase for all metrics tables."""

import json
from collections import OrderedDict
from datetime import date, datetime

from dateutil.tz import tzutc
from flask_restplus import Model, fields
from marshmallow import Schema
from sqlalchemy import MetaData, Column, BigInteger, text
from sqlalchemy import inspect
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.types import TypeDecorator, SmallInteger

# Do not use the cls=xxxx parameter, create a mixin class and add them directly
# to the models.
BaseModel = declarative_base(metadata=MetaData(schema='rdrv2'))

# MetricsBase is the parent for all models in the "metrics" DB. These are
# collected separately for DB migration purposes.
BaseMetricsModel = declarative_base(metadata=MetaData(schema='metricsv2'))


class ModelEnum(TypeDecorator):
    """A type for a SQLAlchemy column based on a protomsg Enum provided in the constructor"""
    impl = SmallInteger

    def __init__(self, enum_type):
        super(ModelEnum, self).__init__()
        self.enum_type = enum_type

    def __repr__(self):
        return "ModelEnum(%s)" % self.enum_type.__name__

    def process_bind_param(self, value, dialect):  # pylint: disable=unused-argument
        return int(value) if value else None

    def process_result_value(self, value, dialect):  # pylint: disable=unused-argument
        return self.enum_type(value) if value else None


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


BaseApiSchema = Model('BaseSchema', {
    # 'status': fields.String(readonly=True),
    # 'error': fields.String(readonly=True),
    'pkId': fields.Integer(readonly=True),
    'created': fields.DateTime(dt_format='iso8601', readonly=True),
    'modified': fields.DateTime(dt_format='iso8601', readonly=True)
})


class ModelMixin(object):
    """
    Base Mixin for all models. Includes methods for importing/exporting JSON data.
    """

    # TODO: Remove if we don't end up using marshmallow.
    __marshmallow__: Schema()

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

        # TODO: Needs to identify ModelEnum fields and set the Enum value from a string.

        """
        if args is not None and len(args) is not 0 and args[0] is not None:
            for key, value in args[0].items():
                self.__dict__[key] = value
                # print('{0} : {1}'.format(key, value))

        else:
            for key, value in kwargs.items():
                self.__dict__[key] = value
                # print('{0} : {1}'.format(key, value))

    def to_json(self, pretty=False):
        """
        Dump class to json string
        :return: json string
        """

        def json_serial(obj):
            """JSON serializer for objects not serializable by default json code"""

            if isinstance(obj, (datetime, date)):
                return obj.isoformat()
            return obj.__repr__()

        data = self.to_dict()

        if pretty:
            output = json.dumps(data, default=json_serial, indent=4)
        else:
            output = json.dumps(data, default=json_serial)

        return output

    def to_dict(self):
        """
        Dump class to python dict
        :return: dict
        """
        data = OrderedDict()
        mapper = inspect(self)

        for column in mapper.attrs:
            key = str(column.key)
            value = getattr(self, key)

            if isinstance(value, (datetime, date)):
                data[key] = value.isoformat()
            # Check for ModelEnum and return name
            elif hasattr(value, 'name') and hasattr(value, 'value'):
                data[key] = value.name
            else:
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
