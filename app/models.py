from datetime import datetime
from typing import Literal

from sqlalchemy import (
    TIMESTAMP,
    Column,
    ForeignKey,
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
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


job_contact = Table(
    "job_contact",
    Base.metadata,
    Column("job_id", ForeignKey("jobs.id"), primary_key=True),
    Column("contact_id", ForeignKey("contacts.id"), primary_key=True),
    ForeignKeyConstraint(["job_id"], ["jobs.id"]),
    ForeignKeyConstraint(["contact_id"], ["contacts.id"]),
    PrimaryKeyConstraint("job_id", "contact_id"),
)

job_note = Table(
    "job_note",
    Base.metadata,
    Column("job_id", ForeignKey("jobs.id"), primary_key=True),
    Column("note_id", ForeignKey("notes.id"), primary_key=True),
    ForeignKeyConstraint(["job_id"], ["jobs.id"]),
    ForeignKeyConstraint(["note_id"], ["notes.id"]),
    PrimaryKeyConstraint("job_id", "note_id"),
)

job_interview = Table(
    "job_interview",
    Base.metadata,
    Column("job_id", ForeignKey("jobs.id"), primary_key=True),
    Column("interview_id", ForeignKey("interviews.id"), primary_key=True),
    ForeignKeyConstraint(["job_id"], ["jobs.id"]),
    ForeignKeyConstraint(["interview_id"], ["interviews.id"]),
    PrimaryKeyConstraint("job_id", "interview_id"),
)

interview_contact = Table(
    "interview_contact",
    Base.metadata,
    Column("interview_id", ForeignKey("interviews.id"), primary_key=True),
    Column("contact_id", ForeignKey("contacts.id"), primary_key=True),
    ForeignKeyConstraint(["interview_id"], ["interviews.id"]),
    ForeignKeyConstraint(["contact_id"], ["contacts.id"]),
    PrimaryKeyConstraint("interview_id", "contact_id"),
)

contact_note = Table(
    "contact_note",
    Base.metadata,
    Column("contact_id", ForeignKey("contacts.id"), primary_key=True),
    Column("note_id", ForeignKey("notes.id"), primary_key=True),
    ForeignKeyConstraint(["contact_id"], ["contacts.id"]),
    ForeignKeyConstraint(["note_id"], ["notes.id"]),
    PrimaryKeyConstraint("contact_id", "note_id"),
)

interview_note = Table(
    "interview_note",
    Base.metadata,
    Column("interview_id", ForeignKey("interviews.id"), primary_key=True),
    Column("note_id", ForeignKey("notes.id"), primary_key=True),
    ForeignKeyConstraint(["interview_id"], ["interviews.id"]),
    ForeignKeyConstraint(["note_id"], ["notes.id"]),
    PrimaryKeyConstraint("interview_id", "note_id"),
)
