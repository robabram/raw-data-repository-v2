from sqlalchemy import Column, Integer, String, UnicodeText, Boolean, UniqueConstraint
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import backref, relationship

from rdr_server.common.enums import CodeType
from rdr_server.model.base_model import BaseModel, ModelMixin, ModelEnum


class CodeBook(ModelMixin, BaseModel):
    """A book of codes.

    Code books contain a list of codes that are referenced in questionnaire concepts,
    questionnaire questions, and questionnaire response answers. They are also used in participant
    summaries and metrics, in place of where an enum field might go otherwise.

    Each import of a code book gets a new ID. All codes that were already in the database are updated
    to have the new code book ID and attributes specified in the code book. Any codes in the code
    book that are missing from the database are inserted. Existing codes that are not in the code
    book are left untouched.
    """
    __tablename__ = 'code_book'
    codeBookId = Column('code_book_id', Integer, unique=True)
    # created = Column('created', UTCDateTime, nullable=False)
    # True if this is the latest imported code book.
    latest = Column('latest', Boolean, nullable=False)
    name = Column('name', String(80), nullable=False)
    system = Column('system', String(255), nullable=False)
    version = Column('version', String(80), nullable=False)

    __table_args__ = (
        UniqueConstraint('system', 'version'),
    )


class _CodeBase(ModelMixin):
    """Mixin with shared columns for Code and CodeHistory"""
    codeId = Column('code_id', Integer, unique=True)
    system = Column('system', String(255), nullable=False)
    value = Column('value', String(80), nullable=False)
    # OMOP codes are supposed to be at most 50 characters long; for legacy codes that exceeded this
    # limit, we populate a shortened version for use in OMOP here. Otherwise, shortValue is identical
    # to value.
    shortValue = Column('short_value', String(50))
    display = Column('display', UnicodeText)
    topic = Column('topic', UnicodeText)
    codeType = Column('code_type', ModelEnum(CodeType), nullable=False)
    mapped = Column('mapped', Boolean, nullable=False)
    # created = Column('created', UTCDateTime, nullable=False)

    @declared_attr
    def codeBookId(cls):
        return Column('code_book_id', Integer, ForeignKey('code_book.code_book_id'))

    @declared_attr
    def parentId(cls):
        return Column('parent_id', Integer, ForeignKey('code.code_id'))


class Code(_CodeBase, BaseModel):
    """A code for a module, question, or answer.

    Questions have modules for parents, and answers have questions for parents.
    """
    __tablename__ = 'code'

    @declared_attr
    def children(cls):
        return relationship(
            cls.__name__,
            backref=backref(
                'parent',
                remote_side='Code.codeId'
            ),
            cascade='all, delete-orphan'
        )

    __table_args__ = (
        UniqueConstraint('system', 'value'),
    )


class CodeHistory(_CodeBase, BaseModel):
    """A version of a code.

    New versions are inserted every time a code book is imported.

    At the moment, CodeHistory is not exposed by any endpoints, and is intended as a historical
    record of codes in case we need it in future.
    """
    __tablename__ = 'code_history'

    # Since codeBookId is nullable, it can't be a part of the primary key; instead create a
    # separate PK for CodeHistory.
    codeHistoryId = Column('code_history_id', Integer, unique=True)
    codeId = Column('code_id', Integer)

    __table_args__ = (
        UniqueConstraint('code_book_id', 'system', 'value', name='uidx_cbid_system_value'),
        UniqueConstraint('code_book_id', 'code_id', name='uidx_cbid_code_id'),
    )
