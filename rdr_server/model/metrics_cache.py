from datetime import datetime

from sqlalchemy import Column, Integer, Date, String, UniqueConstraint

from rdr_server.model.base_model import BaseModel, UTCDateTime


class MetricsEnrollmentStatusCache(BaseModel):
    """Contains enrollment status metrics data grouped by HPO ID and date.
    """
    __tablename__ = 'metrics_enrollment_status_cache'

    dateInserted = Column('date_inserted', UTCDateTime, default=datetime.utcnow(), nullable=False)
    hpoId = Column('hpo_id', String(20), nullable=False)
    hpoName = Column('hpo_name', String(255), nullable=False)
    date = Column('date', Date, nullable=False)
    registeredCount = Column('registered_count', Integer, nullable=False)
    consentedCount = Column('consented_count', Integer, nullable=False)
    coreCount = Column('core_count', Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('date_inserted', 'hpo_id', 'hpo_name', 'date'),
    )


class MetricsRaceCache(BaseModel):
    """Contains race metrics data grouped by HPO ID and date.
    """
    __tablename__ = 'metrics_race_cache'

    dateInserted = Column('date_inserted', UTCDateTime, default=datetime.utcnow(), nullable=False)
    hpoId = Column('hpo_id', String(20), nullable=False)
    hpoName = Column('hpo_name', String(255), nullable=False)
    date = Column('date', Date, nullable=False)
    americanIndianAlaskaNative = Column('american_indian_alaska_native', Integer, nullable=False)
    asian = Column('asian', Integer, nullable=False)
    blackAfricanAmerican = Column('black_african_american', Integer, nullable=False)
    middleEasternNorthAfrican = Column('middle_eastern_north_african', Integer, nullable=False)
    nativeHawaiianOtherPacificIslander = Column('native_hawaiian_other_pacific_islander', Integer,
                                                nullable=False)
    white = Column('white', Integer, nullable=False)
    hispanicLatinoSpanish = Column('hispanic_latino_spanish', Integer, nullable=False)
    noneOfTheseFullyDescribeMe = Column('none_of_these_fully_describe_me', Integer, nullable=False)
    preferNotToAnswer = Column('prefer_not_to_answer', Integer, nullable=False)
    multiAncestry = Column('multi_ancestry', Integer, nullable=False)
    noAncestryChecked = Column('no_ancestry_checked', Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('date_inserted', 'hpo_id', 'hpo_name', 'date'),
    )


class MetricsGenderCache(Base):
    """Contains gender metrics data grouped by HPO ID and date.
    """
    __tablename__ = 'metrics_gender_cache'
    dateInserted = Column('date_inserted', UTCDateTime, default=datetime.utcnow(),
                          nullable=False, primary_key=True)
    hpoId = Column('hpo_id', String(20), primary_key=True)
    hpoName = Column('hpo_name', String(255), primary_key=True)
    date = Column('date', Date, nullable=False, primary_key=True)
    genderName = Column('gender_name', String(255), primary_key=True)
    genderCount = Column('gender_count', Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('date_inserted', 'hpo_id', 'hpo_name', 'date', 'gender_name'),
    )


class MetricsAgeCache(BaseModel):
    """Contains age range metrics data grouped by HPO ID and date.
    """
    __tablename__ = 'metrics_age_cache'

    dateInserted = Column('date_inserted', UTCDateTime, default=datetime.utcnow(), nullable=False)
    hpoId = Column('hpo_id', String(20), nullable=False)
    hpoName = Column('hpo_name', String(255), nullable=False)
    date = Column('date', Date, nullable=False)
    ageRange = Column('age_range', String(255), nullable=False)
    ageCount = Column('age_count', Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('date_inserted', 'hpo_id', 'hpo_name', 'date', 'age_range'),
    )
