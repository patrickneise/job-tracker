from datetime import datetime

from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

from .mixins import TimestampMixin


class Interview(Base, TimestampMixin):
    __tablename__ = "interviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    start: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    stop: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    url: Mapped[str]
    details: Mapped[str]
