from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, HttpUrl, field_serializer

from app.utils import as_form


class ContactBase(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    linkedin: HttpUrl | None = None

    @field_serializer("linkedin")
    def serialize_linkedin(self, linkedin: HttpUrl, _info):
        return str(linkedin)


@as_form
class ContactCreate(ContactBase): ...


@as_form
class ContactUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    linkedin: HttpUrl | None = None


class Contact(ContactBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

    created_at: datetime
    updated_at: datetime
