from typing import List

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import models
from app.contacts.models import Contact
from app.interviews.models import Interview
from app.notes.models import Note


class Job(models.Base, models.TimestampMixin):
    __tablename__ = "jobs"
    __table_args__ = (UniqueConstraint("company", "title"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    company: Mapped[str]
    title: Mapped[str]
    description: Mapped[str]
    posting: Mapped[str]
    website: Mapped[str]

    status: Mapped[models.Status]
    interviews: Mapped[List["Interview"]] = relationship(
        "Interview", secondary=models.job_interview
    )
    contacts: Mapped[List["Contact"]] = relationship(
        "Contact", secondary=models.job_contact
    )
    notes: Mapped[List["Note"]] = relationship("Note", secondary=models.job_note)
