from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.utils import as_form


class NoteBase(BaseModel):
    note: str


@as_form
class NoteCreateUpdate(NoteBase): ...


class Note(NoteBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    html: str
    created_at: datetime
    updated_at: datetime
