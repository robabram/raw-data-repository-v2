#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#
import os

from marshmallow_sqlalchemy import ModelConversionError, ModelSchema
from sqlalchemy import event
from sqlalchemy.orm import mapper
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.session import Session

from rdr_server.model.base_database import Database
from rdr_server.model.base_model import BaseModel, BaseMetricsModel

if 'DB_CONNECTION_STRING' in os.environ:
    _conn_url = os.getenv('DB_CONNECTION_STRING')
else:
    _conn_url = 'mysql+mysqldb://rdr:rdr!pwd@localhost/rdr?charset=utf8'

_database = Database(_conn_url)


def setup_schema(BaseDao, session):
    """
    Create a function which incorporates the Base and session information.
    Marshmallow schemas can be accessed from any Model object:
       schema = Model.__marshmallow__()
       schema = obj.__class__.__marshmallow__()
    Note: Model.__marshmallow__ returns the Class not an instance of the schema so remember to instantiate it.
    :param BaseDao: Base sqlalchemy object created from declarative_base()
    :param session: Database session object
    :return: function
    """
    def setup_schema_fn():
        for class_ in BaseDao._decl_class_registry.values():
            if hasattr(class_, '__tablename__'):
                if class_.__name__.endswith('Schema'):
                    raise ModelConversionError(
                        "For safety, setup_schema can not be used when a"
                        "Model class ends with 'Schema'"
                    )

                class Meta(object):
                    model = class_
                    sqla_session = session
                    dump_only = ('pkId', 'created', 'modified')

                schema_class_name = '%sSchema' % class_.__name__

                schema_class = type(
                    schema_class_name,
                    (ModelSchema,),
                    {'Meta': Meta}
                )

                setattr(class_, '__marshmallow__', schema_class)

    return setup_schema_fn


# Listen for the SQLAlchemy event and run setup_schema.
# Note: This has to be done after Base and session are setup
event.listen(mapper, 'after_configured', setup_schema(BaseModel, _database.session()))
event.listen(mapper, 'after_configured', setup_schema(BaseMetricsModel, _database.session()))


class BaseDao(object):

    model: object = None
    _database = None

    def __init__(self, model: object):

        self.model = model
        self._database = _database

    def session(self) -> Session:
        return self._database.session()

    def get_query(self, session: Session, *args) -> Query:
        """
        Return a Query object initialized with our model
        :param session: Session object
        :return: Query object
        """
        if session is None:
            raise ValueError('invalid session object')

        # https://docs.sqlalchemy.org/en/latest/orm/query.html#the-query-object
        if args:
            return Query(*args, session=session)
        return Query(self.model, session=session)

    def count(self):
        """
        Return the number of records in the model
        :return: record count
        """
        if not self.model:
            raise NameError('database model has not been set.')

        with self.session() as session:
            query = self.get_query(session)
            data = query.count()
            return data

    def list(self):
        """
        Return a list of all records
        :return: list of records
        """
        if not self.model:
            raise NameError('database model has not been set.')

        with self.session() as session:
            query = self.get_query(session)
            data = query.all()
            return data

    def get_by_id(self, pkId: int):
        """
        Return a record identified by the primary key id
        :param pk_id: primary key id
        :return: a single record
        """
        if not self.model:
            raise NameError('database model has not been set.')
        if not pkId:
            raise ValueError('invalid primary key value.')

        with self.session() as session:
            query = self.get_query(session)
            rec = query.get(pkId)
            return rec

    def delete_by_id(self, pkId: int):
        """
        Delete a record using the primary key value
        :param pk_id: primary key id
        """
        if not self.model:
            raise NameError('database model has not been set.')
        if not pkId:
            raise ValueError('invalid primary key value.')

        with self.session() as session:
            query = self.get_query(session)
            query.filter(self.model.pkId == pkId).delete()

    def base_fields(self):
        """
        Return the base model fields
        :return: list of records
        """
        if not self.model:
            raise NameError('database model has not been set.')

        with self.session() as session:
            query = self.get_query(session, [self.model.pkId, self.model.created, self.model.modified])
            data = query.order_by(self.model.pkId).all()
            return data

    def insert(self, data):
        """
        Insert a new record into the model
        :param data: json data
        """

        if not data:
            raise ValueError('invalid data')

        # TODO: validate and insert data into model

