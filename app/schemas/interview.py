from __future__ import annotations

from datetime import datetime
from typing import List

from fastapi import Form
from pydantic import BaseModel, ConfigDict, HttpUrl

from app.schemas.contact import Contact
from app.schemas.note import Note


class InterviewBase(BaseModel):
    start: datetime
    stop: datetime
    details: str
    url: HttpUrl | None = None


class InterviewCreate(InterviewBase):
    @classmethod
    def as_form(
        cls,
        start: datetime = Form(...),
        stop: datetime = Form(...),
        details: str = Form(...),
        url: HttpUrl = Form(...),
    ) -> InterviewCreate:
        return cls(start=start, stop=stop, details=details, url=url)


class InterviewUpdate(InterviewBase):
    start: datetime | None = None
    stop: datetime | None = None
    details: str | None = None
    url: HttpUrl | None = None

    @classmethod
    def as_form(
        cls,
        start: datetime | None = Form(...),
        stop: datetime | None = Form(...),
        details: str | None = Form(...),
        url: HttpUrl | None = Form(...),
    ) -> InterviewUpdate:
        return cls(start=start, stop=stop, details=details, url=url)


class Interview(InterviewBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    contacts: List[Contact]
    notes: List[Note]
