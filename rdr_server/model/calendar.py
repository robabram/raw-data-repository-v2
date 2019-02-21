from flask_restplus import fields
from sqlalchemy import Date, Column

from rdr_server.model.base_model import BaseModel, ModelMixin, BaseApiSchema


class Calendar(ModelMixin, BaseModel):
    __tablename__ = 'calendar'
    day = Column('day', Date, unique=True)


CalendarApiSchema = BaseApiSchema.clone('Calendar', {
    'day': fields.Date(required=True, description='Date value')
})
