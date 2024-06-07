from datetime import datetime
from typing import List, Literal, Optional

from sqlalchemy import TIMESTAMP, Column, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .database import Base


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
)


class Job(Base, TimestampMixin):
    __tablename__ = "jobs"
    __table_args__ = (UniqueConstraint("company", "title"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    company: Mapped[str]
    title: Mapped[str]
    description: Mapped[str]
    posting: Mapped[str]
    website: Mapped[str]

    status: Mapped[Status]
    contacts: Mapped[List["Contact"]] = relationship(
        secondary=job_contact, back_populates="jobs"
    )


class Contact(Base, TimestampMixin):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    phone: Mapped[Optional[str]]
    linkedin: Mapped[Optional[str]]

    jobs: Mapped[List["Job"]] = relationship(
        secondary=job_contact, back_populates="contacts"
    )
