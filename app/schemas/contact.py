from __future__ import annotations

from datetime import datetime

from fastapi import Form
from pydantic import BaseModel, ConfigDict, EmailStr, HttpUrl


class ContactBase(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    linkedin: HttpUrl | None = None


class ContactCreate(ContactBase):
    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        email: EmailStr = Form(...),
        phone: str = Form(...),
        linkedin: HttpUrl = Form(...),
    ) -> ContactCreate:
        return cls(name=name, email=email, phone=phone, linkedin=linkedin)


class ContactUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    linkedin: HttpUrl | None = None

    @classmethod
    def as_form(
        cls,
        name: str | None = Form(...),
        email: EmailStr | None = Form(...),
        phone: str | None = Form(...),
        linkedin: HttpUrl | None = Form(...),
    ) -> ContactUpdate:
        return cls(name=name, email=email, phone=phone, linkedin=linkedin)


class Contact(ContactBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

    created_at: datetime
    updated_at: datetime
