from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, HttpUrl, field_serializer

from app.domain.contacts.schema import Contact
from app.domain.notes.schema import Note
from app.utils import as_form


class InterviewBase(BaseModel):
    start: datetime
    stop: datetime
    details: str
    url: HttpUrl | None = None

    @field_serializer("url")
    def serialize_url(self, url: HttpUrl, _info):
        return str(url)


@as_form
class InterviewCreate(InterviewBase): ...


@as_form
class InterviewUpdate(InterviewBase):
    start: datetime | None = None
    stop: datetime | None = None
    details: str | None = None
    url: HttpUrl | None = None


class Interview(InterviewBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    contacts: List[Contact]
    notes: List[Note]
