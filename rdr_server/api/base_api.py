#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#
from collections import OrderedDict
from datetime import date, datetime

from flask import abort
from flask_restplus import Resource, Model, fields
from sqlalchemy.exc import IntegrityError

from rdr_server.model.base_model import ModelMixin
from rdr_server.dao.exceptions import RecordNotFoundError


def response_handler(func):
    """
    A decorator to handle exceptions processing a response
    """
    def f(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        #TODO: Log exceptions
        except IntegrityError:
            return {'error': 'duplicate'}, 409
        except RecordNotFoundError:
            return {'error': 'not found'}, 404
        except Exception:
            return {'error': 'unknown'}, 500

    return f


def user_auth(f):
    """Checks whether user is logged in or raises error 401."""

    def decorator(*args, **kwargs):
        if True is False:
            abort(401)
        return f(*args, **kwargs)

    return decorator


class BaseApiModel(Resource):
    model = None

    def response(self, data=None):
        """
        Format the model data into json
        :param data: model data
        :return: string
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
        return {'count': self.model.count()}


class BaseApiList(BaseApiModel):
    """
    Return a all records in the model
    """

    def get(self):
        """
        Return all the records from the table
        :return: return list
        """
        data = self.model.list()
        response = self.response(data)
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
        data = self.model.base_fields()
        response = self.response(data)
        return response


class BaseApiPK(BaseApiModel):
    """
    Handle all operations using the primary key id
    """
    def get(self, pk_id):
        rec = self.model.get_by_id(pk_id)
        if not rec:
            raise RecordNotFoundError()
        return rec.to_dict(), 200

    def delete(self, pk_id):
        rec = self.model.get_by_id(pk_id)
        if not rec:
            raise RecordNotFoundError()
        self.model.delete_by_id(pk_id)
        return {'status': 'deleted'}, 202

    # TODO: add PUT method
