from sqlalchemy.orm import Mapped, mapped_column

from app import models


class Note(models.Base, models.TimestampMixin):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    note: Mapped[str]
    html: Mapped[str]
