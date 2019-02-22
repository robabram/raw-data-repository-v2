#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#
from collections import OrderedDict
from datetime import date, datetime

from flask import Response, abort
from flask_restplus import Resource
from sqlalchemy.exc import IntegrityError

from rdr_server.dao.exceptions import RecordNotFoundError
from rdr_server.model.base_model import ModelMixin


def response_handler(func):
    """
    A decorator to handle exceptions processing a response
    """

    def f(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        # TODO: Log exceptions
        except IntegrityError:
            abort(409, 'duplicate')
        except RecordNotFoundError:
            abort(404, 'not found')
        except Exception:
            abort(500, 'server error')

    return f


def user_auth(f):
    """Checks whether user is logged in or raises error 401."""

    def decorator(*args, **kwargs):
        if True is False:
            abort(401)
        return f(*args, **kwargs)

    return decorator


class BaseApiModel(Resource):
    dao = None

    def to_dict(self, data=None):
        """
        Convert sqlalchemy models/result objects into a python dict
        :param data: Result data
        :return: dict
        """
        if not data or (isinstance(data, list) and len(data) == 0):
            return dict()

        results = dict()

        if isinstance(data, list):
            results = list()
            obj = data[0]

            # determine if this is a simple result object.
            if hasattr(obj, '_fields'):

                # loop through the items, converting the result object to a dict
                for item in data:
                    od = OrderedDict()

                    for key in getattr(obj, '_fields'):

                        value = getattr(item, key)
                        if isinstance(value, (datetime, date)):
                            od[key] = value.isoformat()
                        else:
                            od[key] = value

                    results.append(od)

            # determine if this is a model object
            if isinstance(obj, ModelMixin):
                for item in data:
                    results.append(item.to_dict())

        # TODO: Do we need to handle single model records or result objects here?

        return results


class BaseApiCount(BaseApiModel):

    def get(self):
        """
        Return the count of all recors in the table
        :return: integer
        """
        return {'count': self.dao.count()}


class BaseApiList(BaseApiModel):
    """
    Return a all records in the model
    """

    def get(self):
        """
        Return all the records from the table
        :return: return list
        """
        data = self.dao.list()
        response = self.to_dict(data)
        return response


class BaseApiSync(BaseApiModel):
    """
    Return the base model fields
    """

    def get(self):
        """
        Return the basic record information for all records.
        :return: return list
        """
        data = self.dao.base_fields()
        response = self.to_dict(data)
        return response


class BaseApiPK(BaseApiModel):
    """
    Handle all operations using the primary key id
    """

    def get(self, pk_id):
        rec = self.dao.get_by_id(pk_id)
        if not rec:
            raise RecordNotFoundError()
        return rec.to_dict(), 200

    def delete(self, pk_id):
        rec = self.dao.get_by_id(pk_id)
        if not rec:
            raise RecordNotFoundError()
        self.dao.delete_by_id(pk_id)
        return {'status': 'deleted'}, 202

    # TODO: add PUT method
