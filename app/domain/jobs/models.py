from __future__ import annotations

from typing import List

from sqlalchemy import String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import models
from app.domain.contacts.models import Contact
from app.domain.interviews.models import Interview
from app.domain.notes.models import Note


class Job(models.Base, models.TimestampMixin):
    __tablename__ = "jobs"
    __table_args__ = (UniqueConstraint("company", "title"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    company: Mapped[str] = mapped_column(String(80))
    title: Mapped[str] = mapped_column(String(80))
    description: Mapped[str] = mapped_column(Text)
    posting: Mapped[str]
    website: Mapped[str]
    status: Mapped[models.Status]

    interviews: Mapped[List[Interview]] = relationship(
        "Interview", back_populates="jobs"
    )
    contacts: Mapped[List[Contact]] = relationship(
        secondary="job_contact", back_populates="jobs"
    )
    notes: Mapped[List[Note]] = relationship(
        "Note", secondary="job_note", back_populates="jobs"
    )
