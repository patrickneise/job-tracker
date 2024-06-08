from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

from .mixins import TimestampMixin


class Note(Base, TimestampMixin):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    note: Mapped[str]
    html: Mapped[str]
