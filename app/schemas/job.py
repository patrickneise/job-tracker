from __future__ import annotations

from datetime import datetime
from typing import List

from fastapi import Form
from pydantic import BaseModel, ConfigDict, HttpUrl, field_serializer

from app.models.mixins import Status
from app.schemas.contact import Contact
from app.schemas.note import Note
from app.schemas.utils import as_form


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


# class JobCreate(JobBase):
#     @classmethod
#     def as_form(
#         cls,
#         company: str = Form(...),
#         title: str = Form(...),
#         description: str = Form(...),
#         posting: HttpUrl = Form(...),
#         website: HttpUrl = Form(...),
#         status: Status = Form(...),
#     ) -> JobCreate:
#         return cls(
#             company=company,
#             title=title,
#             description=description,
#             posting=posting,
#             website=website,
#             status=status,
#         )


class JobUpdate(BaseModel):
    company: str | None = None
    title: str | None = None
    description: str | None = None
    posting: HttpUrl | None = None
    website: HttpUrl | None = None
    status: Status | None = None

    @classmethod
    def as_form(
        cls,
        company: str | None = Form(...),
        title: str | None = Form(...),
        description: str | None = Form(...),
        posting: HttpUrl | None = Form(...),
        website: HttpUrl | None = Form(...),
        status: Status = Form(...),
    ) -> JobUpdate:
        return cls(
            company=company,
            title=title,
            description=description,
            posting=posting,
            website=website,
            status=status,
        )


class Job(JobBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

    created_at: datetime
    updated_at: datetime

    contacts: List[Contact]
    notes: List[Note]
