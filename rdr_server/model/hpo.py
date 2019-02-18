from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from rdr_server.common.system_enums import OrganizationType, ObsoleteStatus
from rdr_server.model.base_model import BaseModel


class HPO(BaseModel):
    """An awardee, containing organizations (which in turn contain sites.)"""
    __tablename__ = 'hpo'

    hpoId = Column('hpo_id', Integer, unique=True, autoincrement=False)
    name = Column('name', String(20), unique=True)
    displayName = Column('display_name', String(255))
    organizationType = Column('organization_type', Enum(OrganizationType),
                              default=OrganizationType.UNSET)
    organizations = relationship('Organization', cascade='all, delete-orphan',
                                 order_by='Organization.externalId')
    isObsolete = Column('is_obsolete', Enum(ObsoleteStatus))
