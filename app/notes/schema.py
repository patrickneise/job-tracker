from __future__ import annotations

from datetime import datetime

from fastapi import Form
from pydantic import BaseModel, ConfigDict


class NoteBase(BaseModel):
    note: str


class NoteCreateUpdate(NoteBase):
    @classmethod
    def as_form(
        cls,
        note: str = Form(...),
    ) -> NoteCreateUpdate:
        return cls(note=note)


class Note(NoteBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    html: str
    created_at: datetime
    updated_at: datetime
