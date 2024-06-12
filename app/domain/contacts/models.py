from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import models

if TYPE_CHECKING:
    from app.domain.interviews.models import Interview
    from app.domain.jobs.models import Job
    from app.domain.notes.models import Note
else:
    Interview = "Interview"
    Job = "Job"
    Note = "Note"


class Contact(models.Base, models.TimestampMixin):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[Optional[str]]
    linkedin: Mapped[Optional[str]]

    jobs: Mapped[List[Job]] = relationship(
        "Job", secondary="job_contact", back_populates="contacts"
    )
    interviews: Mapped[List[Interview]] = relationship(
        "Interview", secondary="interview_contact", back_populates="contacts"
    )
    notes: Mapped[List[Note]] = relationship(
        "Note", secondary="contact_note", back_populates="contacts"
    )
