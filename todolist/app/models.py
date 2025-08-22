from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Enum as SqlEnum,
)
from sqlalchemy.sql import func
from ..utils import enum
from .database import Base


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    priority = Column(
        SqlEnum(enum.PriorityEnum),
        nullable=False,
        default=enum.PriorityEnum.MEDIUM,
    )
    category = Column(
        SqlEnum(enum.CategoryEnum),
        nullable=False,
        default=enum.CategoryEnum.WORK,
    )
    due_date = Column(DateTime, nullable=True)
    recurrence = Column(
        SqlEnum(enum.RecurrenceEnum),
        nullable=False,
        default=enum.RecurrenceEnum.NONE,
    )
    completed = Column(Boolean, nullable=False, default=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


