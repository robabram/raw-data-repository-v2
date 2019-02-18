from datetime import datetime
from sqlalchemy import Column, Integer, BLOB, Boolean, Date, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from rdr_server.model.base_model import BaseModel, UTCDateTime


BUCKETS = {'buckets': {}}


class MetricsVersion(BaseModel):
    """A version containing a set of metrics in the database, generated by a pipeline.

    Contains buckets with metrics grouped by HPO ID and date.
    """
    __tablename__ = 'metrics_version'

    metricsVersionId = Column('metrics_version_id', Integer, unique=True)
    inProgress = Column('in_progress', Boolean, default=False, nullable=False)
    complete = Column('complete', Boolean, default=False, nullable=False)
    date = Column('date', UTCDateTime, default=datetime.utcnow(), nullable=False)
    dataVersion = Column('data_version', Integer, nullable=False)
    buckets = relationship('MetricsBucket', cascade='all, delete-orphan', passive_deletes=True)


class MetricsBucket(BaseModel):
    """A bucket belonging to a MetricsVersion, containing metrics for a particular HPO ID and date.
    """
    __tablename__ = 'metrics_bucket'

    metricsVersionId = Column('metrics_version_id', Integer,
                              ForeignKey('metrics_version.metrics_version_id', ondelete='CASCADE'))
    date = Column('date', Date)
    hpoId = Column('hpo_id', String(20))  # Set to '' for cross-HPO metrics
    metrics = Column('metrics', BLOB, nullable=False)

    __table_args__ = (
        UniqueConstraint('metrics_version_id', 'date', 'hpo_id', name='uidx_version_date_hpoid'),
    )
