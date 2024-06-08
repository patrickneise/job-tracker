from typing import List

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

from .association_tables import job_contact, job_interview, job_note
from .contact import Contact
from .interview import Interview
from .mixins import Status, TimestampMixin
from .note import Note


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
    interviews: Mapped[List["Interview"]] = relationship(
        "Interview", secondary=job_interview
    )
    contacts: Mapped[List["Contact"]] = relationship("Contact", secondary=job_contact)
    notes: Mapped[List["Note"]] = relationship("Note", secondary=job_note)
