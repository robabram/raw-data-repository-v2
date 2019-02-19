#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#
import os
from sqlalchemy.orm.session import Session
from rdr_server.model.base_database import Database


class BaseDao(object):

    model = None
    _database = None

    def __init__(self, model=None):

        self.model = model

        if 'DB_CONNECTION_STRING' in os.environ:
            conn_url = os.getenv('DB_CONNECTION_STRING')
        else:
            conn_url = 'mysql+mysqldb://rdr:rdr!pwd@localhost/rdr?charset=utf8'

        self._database = Database(conn_url)

    def session(self) -> Session:
        return self._database.session()

    def count(self):
        """
        Return the number of records in the model
        :return: record count
        """
        if not self.model:
            raise NameError('database model has not been set')

        with self.session() as session:
            return session.query(self.model.pkId).count()

