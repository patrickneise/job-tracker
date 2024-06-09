from datetime import datetime
from typing import List

from sqlalchemy import TIMESTAMP, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import models
from app.contacts.models import Contact
from app.notes.models import Note


class Interview(models.Base, models.TimestampMixin):
    __tablename__ = "interviews"
    __table_args__ = (UniqueConstraint("start", "stop"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    start: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    stop: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    details: Mapped[str] = mapped_column(Text)
    url: Mapped[str]

    contacts: Mapped[List["Contact"]] = relationship(
        "Contact", secondary=models.interview_contact
    )
    notes: Mapped[List["Note"]] = relationship("Note", secondary=models.interview_note)
