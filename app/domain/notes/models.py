from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from app import models


class Note(models.Base, models.TimestampMixin):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    note: Mapped[str] = mapped_column(Text)
    html: Mapped[str] = mapped_column(Text)
