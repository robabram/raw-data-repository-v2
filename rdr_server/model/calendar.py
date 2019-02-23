
from flask_restplus import fields
from sqlalchemy import Date, Column
from rdr_server.model.base_model import ModelEnum

from rdr_server.model.base_model import BaseModel, ModelMixin, BaseApiSchema
from rdr_server.common.enums import EnrollmentStatus, SampleStatus


class Calendar(ModelMixin, BaseModel):
    __tablename__ = 'calendar'
    day = Column('day', Date, unique=True)
    enrollmentStatus = Column('enrollment_status', ModelEnum(EnrollmentStatus))
    SampleStatus = Column('sample_status', ModelEnum(SampleStatus))


CalendarApiSchema = BaseApiSchema.clone('Calendar', {
    'day': fields.Date(required=True, description='Date value'),
    'enrollmentStatus': fields.String(description='Participant Enrollment Status'),
    'sampleStatus': fields.String(description='BioBank Sample Status')
})
