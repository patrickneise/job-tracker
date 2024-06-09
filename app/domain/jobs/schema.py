from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, HttpUrl, field_serializer

from app.contacts.schema import Contact
from app.interviews.schema import Interview
from app.models import Status
from app.notes.schema import Note
from app.utils import as_form


class JobBase(BaseModel):
    company: str
    title: str
    description: str
    posting: HttpUrl
    website: HttpUrl
    status: Status

    @field_serializer("posting")
    def serialize_posting(self, posting: HttpUrl, _info):
        return str(posting)

    @field_serializer("website")
    def serialize_website(self, website: HttpUrl, _info):
        return str(website)


@as_form
class JobCreate(JobBase): ...


@as_form
class JobUpdate(JobBase):
    company: str | None = None
    title: str | None = None
    description: str | None = None
    posting: HttpUrl | None = None
    website: HttpUrl | None = None
    status: Status | None = None


class Job(JobBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

    created_at: datetime
    updated_at: datetime

    contacts: List[Contact]
    interviews: List[Interview]
    notes: List[Note]
