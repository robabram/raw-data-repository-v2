from sqlalchemy import Date, Column

from rdr_server.model.base_model import BaseModel, ModelMixin


class Calendar(ModelMixin, BaseModel):
    __tablename__ = 'calendar'
    day = Column('day', Date, unique=True)

