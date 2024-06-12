from __future__ import annotations

from typing import TYPE_CHECKING, List

import markdown
from sqlalchemy import Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import models

if TYPE_CHECKING:
    from app.domain.contacts.models import Contact
    from app.domain.interviews.models import Interview
    from app.domain.jobs.models import Job
else:
    Contact = "Contact"
    Interview = "Interview"
    Job = "Job"


def note_to_html(context) -> str:
    note = context.current_parameters["note"]
    return markdown.markdown(note)


class Note(models.Base, models.TimestampMixin):
    __tablename__ = "notes"
    __table_args__ = (UniqueConstraint("id", "note"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    note: Mapped[str] = mapped_column(Text)
    html: Mapped[str] = mapped_column(Text, default=note_to_html, onupdate=note_to_html)

    jobs: Mapped[List[Job]] = relationship(
        "Job", secondary="job_note", back_populates="notes"
    )
    interviews: Mapped[List[Interview]] = relationship(
        "Interview", secondary="interview_note", back_populates="notes"
    )
    contacts: Mapped[List[Contact]] = relationship(
        "Contact", secondary="contact_note", back_populates="notes"
    )
