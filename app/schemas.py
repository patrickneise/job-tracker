from __future__ import annotations

from typing import List

from fastapi import Form
from pydantic import BaseModel, ConfigDict

from app.models import Status


class ContactBase(BaseModel):
    name: str
    email: str
    phone: str | None = None
    linkedin: str | None = None


class ContactCreate(ContactBase): ...


class ContactUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    linkedin: str | None = None


class Contact(ContactBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class JobBase(BaseModel):
    company: str
    title: str
    description: str
    posting: str  # TODO: change to URL
    website: str  # TODO: change to URL
    status: Status


class JobCreate(JobBase):
    @classmethod
    def as_form(
        cls,
        company: str = Form(...),
        title: str = Form(...),
        description: str = Form(...),
        posting: str = Form(...),
        website: str = Form(...),
        status: Status = Form(...),
    ) -> JobCreate:
        return cls(
            company=company,
            title=title,
            description=description,
            posting=posting,
            website=website,
            status=status,
        )


class JobUpdate(BaseModel):
    company: str | None = None
    title: str | None = None
    description: str | None = None
    posting: str | None = None
    website: str | None = None
    status: Status | None = None

    @classmethod
    def as_form(
        cls,
        company: str | None = Form(...),
        title: str | None = Form(...),
        description: str | None = Form(...),
        posting: str | None = Form(...),
        website: str | None = Form(...),
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
    contacts: List[Contact]
