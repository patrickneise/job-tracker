from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

from .mixins import TimestampMixin


class Contact(Base, TimestampMixin):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    phone: Mapped[Optional[str]]
    linkedin: Mapped[Optional[str]]
