from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from app import models


class Contact(models.Base, models.TimestampMixin):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    phone: Mapped[Optional[str]]
    linkedin: Mapped[Optional[str]]
