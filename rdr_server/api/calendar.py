#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#
from flask_restplus import Namespace

from rdr_server.api.base_api import BaseApiCount, BaseApiList, BaseApiSync, BaseApiGetId, BaseApiDeleteId, \
    BaseApiPost, BaseApiPut, response_handler
from rdr_server.dao.base_dao import BaseDao
from rdr_server.model.calendar import Calendar, CalendarApiSchema

api = Namespace('calendars', description='Calendar related operations')
api.models[CalendarApiSchema.name] = CalendarApiSchema


@api.route('/count')
class CalendarApiCount(BaseApiCount):

    dao = BaseDao(Calendar)


@api.route('/sync')
class CalendarApiSync(BaseApiSync):

    dao = BaseDao(Calendar)


@api.route('/')
class CalendarApiList(BaseApiList):

    dao = BaseDao(Calendar)


@api.route('/<int:pkId>')
@api.response(404, 'Calendar record not found')
@api.param('pkId', 'Unique record identifier')
class CalendarApiGetId(BaseApiGetId):

    dao = BaseDao(Calendar)

    @api.doc('get calendar record')
    @api.marshal_with(CalendarApiSchema, skip_none=True)
    # @response_handler
    def get(self, pkId):
        return super(CalendarApiGetId, self).get(pkId)


@api.route('/insert')
class CalendarApiPost(BaseApiPost):

    dao = BaseDao(Calendar)

    @api.doc('create_calendar')
    @api.expect(CalendarApiSchema)
    @api.marshal_with(CalendarApiSchema, skip_none=True)
    @response_handler
    def post(self):
        calendar = Calendar(**api.payload)

        with self.dao.session() as session:
            session.add(calendar)
            session.commit()

            # reload calendar record
            calendar = self.dao.get_by_id(calendar.pkId)

            data = self.to_dict(calendar)
            return data, 201


@api.route('/<int:pkId>/update')
@api.response(404, 'Calendar record not found')
@api.param('pkId', 'Unique record identifier')
class CalendarApiPut(BaseApiPut):

    dao = BaseDao(Calendar)

    @api.expect(CalendarApiSchema)
    @api.marshal_with(CalendarApiSchema, skip_none=True)
    @response_handler
    def put(self, pkId):

        calendar = Calendar(**api.payload)
        calendar.pkId = pkId

        with self.dao.session() as session:
            session.add(calendar)
            session.commit()

            # reload calendar record
            calendar = self.dao.get_by_id(calendar.pkId)

            return self.to_dict(calendar), 200


@api.route('/<int:pkId>/delete')
@api.response(404, 'Calendar record not found')
@api.param('pkId', 'Unique record identifier')
class CalendarApiDeleteId(BaseApiDeleteId):

    dao = BaseDao(Calendar)

    @api.doc('Delete a calendar record')
    @response_handler
    def delete(self, pkId):
        return super(CalendarApiDeleteId, self).delete(pkId)
