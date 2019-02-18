from sqlalchemy import Date, Column

from rdr_server.model.base_model import BaseModel


class Calendar(BaseModel):
    __tablename__ = 'calendar'
    day = Column('day', Date, unique=True)

