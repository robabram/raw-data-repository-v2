#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#
from collections import OrderedDict
from datetime import date, datetime
import importlib
import re

from flask import abort
from flask_restplus import Resource
from sqlalchemy.inspection import inspect
from sqlalchemy.exc import IntegrityError

from rdr_server.dao.base_dao import BaseDao
from rdr_server.dao.exceptions import RecordNotFoundError
from rdr_server.model.base_model import ModelMixin, ModelEnum


def response_handler(func):
    """
    A decorator to handle exceptions processing a response
    """

    def f(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        # TODO: Log exceptions here, handle more exception types.
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


class BaseDaoApi(Resource):
    """
    Generic Api Class with support for DAO objects
    """
    dao: BaseDao = None

    def to_dict(self, data=None):
        """
        Convert sqlalchemy models/result objects into a python dict
        :param data: Result data
        :return: dict
        """
        if not data or (isinstance(data, list) and len(data) == 0):
            return dict()

        # handle a list of objects
        if isinstance(data, list):
            results = list()
            obj = data[0]

            # determine if this is a simple Result object.
            if hasattr(obj, '_fields'):

                # loop through the items, converting the result object to a dict
                for result in data:
                    item = self.result_to_dict(result)
                    results.append(item)

                return results

            # determine if this is a model object
            if isinstance(obj, ModelMixin):

                for rec in data:
                    item = self.model_to_dict(rec)
                    results.append(item)

                return results

        # handle a single Result record
        if hasattr(data, '_fields'):
            item = self.result_to_dict(data)
            return item

        # handle a single Model record
        if isinstance(data, ModelMixin):
            item = self.model_to_dict(data)
            return item

        raise ValueError('invalid data, unable to convert to dict()')

    def enum_to_string(self, enum):
        """
        Return the name string of the enum value
        :param enum: Enum object
        :return: String
        """
        value = enum.name
        return value

    def string_to_enum(self, enum, value):
        """
        Return the enum value for a given enum and name string
        :param enum: Enum object
        :param value: Enum item name string
        :return: Enum object
        """
        value = enum[value]
        return value

    def result_to_dict(self, result):
        """
        A Result is row data returned from a custom query.
        :param result: Result object
        :return: dict
        """
        od = OrderedDict()

        for key in getattr(result, '_fields'):

            value = getattr(result, key)
            if isinstance(value, (datetime, date)):
                od[key] = value.isoformat()
            # Check for ModelEnum and return name
            elif hasattr(value, 'name') and hasattr(value, 'value'):
                od[key] = value.name
            else:
                od[key] = value

            # see if this field is an Enum
            pass

        return od

    def model_to_dict(self, model):
        """
        Converts a model to a dict
        :param model: SqlAlchemy Model
        :return: dict
        """
        # to_dict() already handles converting dates and enums
        data = model.to_dict()

        x = self.dict_to_model(data)

        return data

    def dict_to_model(self, data):

        # TODO: Create empty model obj, inspect and look for Enums.
        #  Convert Enum strings to IDs. Insert data into new model and return.

        od = OrderedDict()
        model = self.dao.model()
        info = inspect(model)
        mod = None

        for key, value in data.items():

            class_str = str(info.mapper.columns[key].base_columns)

            if 'ModelEnum' in class_str:
                match = re.match('.*?, ModelEnum\((.*?)\).*', class_str)
                enum_name = match.groups()[0]

                if mod is None:
                    mod = importlib.import_module('rdr_server.common.enums')

                enum = eval('mod.{0}'.format(enum_name))

                od[key] = enum[value]
            else:
                od[key] = value

        return od







class BaseApiCount(BaseDaoApi):

    def get(self):
        """
        Return the count of all recors in the table
        :return: integer
        """
        return {'count': self.dao.count()}, 200


class BaseApiList(BaseDaoApi):
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


class BaseApiSync(BaseDaoApi):
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

# TODO: add PUT method


class BaseApiPut(BaseDaoApi):
    pass


class BaseApiPost(BaseDaoApi):
    pass


class BaseApiGetId(BaseDaoApi):
    """
    Handle get operations using the primary key id
    """

    def get(self, pk_id):
        rec = self.dao.get_by_id(pk_id)
        if not rec:
            raise RecordNotFoundError()
        return self.to_dict(rec), 200


class BaseApiDeleteId(BaseDaoApi):
    """
    Handle DELETE operations using the primary key id
    """

    def delete(self, pk_id):
        rec = self.dao.get_by_id(pk_id)
        if not rec:
            raise RecordNotFoundError()
        self.dao.delete_by_id(pk_id)
        return {'pkId': pk_id}, 200
