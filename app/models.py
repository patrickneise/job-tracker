from datetime import datetime
from typing import Literal

from sqlalchemy import (
    TIMESTAMP,
    Column,
    ForeignKey,
    Table,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase): ...


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )


Status = Literal["watching", "applied", "interview", "offer", "rejected", "stale"]
NOTE_TYPES = Literal["job", "interview", "contact"]

job_contact = Table(
    "job_contact",
    Base.metadata,
    Column("job_id", ForeignKey("jobs.id"), primary_key=True),
    Column("contact_id", ForeignKey("contacts.id"), primary_key=True),
)

job_note = Table(
    "job_note",
    Base.metadata,
    Column("job_id", ForeignKey("jobs.id"), primary_key=True),
    Column("note_id", ForeignKey("notes.id"), primary_key=True),
)

interview_contact = Table(
    "interview_contact",
    Base.metadata,
    Column("interview_id", ForeignKey("interviews.id"), primary_key=True),
    Column("contact_id", ForeignKey("contacts.id"), primary_key=True),
)

contact_note = Table(
    "contact_note",
    Base.metadata,
    Column("contact_id", ForeignKey("contacts.id"), primary_key=True),
    Column("note_id", ForeignKey("notes.id"), primary_key=True),
)

interview_note = Table(
    "interview_note",
    Base.metadata,
    Column("interview_id", ForeignKey("interviews.id"), primary_key=True),
    Column("note_id", ForeignKey("notes.id"), primary_key=True),
)
