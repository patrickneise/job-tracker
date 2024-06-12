from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import TIMESTAMP, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import models

if TYPE_CHECKING:
    from app.domain.contacts.models import Contact
    from app.domain.jobs.models import Job
    from app.domain.notes.models import Note
else:
    Job = "Job"
    Contact = "Contact"
    Note = "Note"


class Interview(models.Base, models.TimestampMixin):
    __tablename__ = "interviews"
    __table_args__ = (UniqueConstraint("start", "stop"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    start: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    stop: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    details: Mapped[str] = mapped_column(Text)
    url: Mapped[str]

    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"))
    jobs: Mapped[Job] = relationship("Job", back_populates="interviews")

    contacts: Mapped[List[Contact]] = relationship(
        "Contact", secondary="interview_contact", back_populates="interviews"
    )
    notes: Mapped[List[Note]] = relationship(
        "Note", secondary="interview_note", back_populates="interviews"
    )
