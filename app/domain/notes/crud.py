from typing import Literal

from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import EntryConflict, EntryNotFound
from app.domain.contacts.models import Contact
from app.domain.interviews.models import Interview
from app.domain.jobs.models import Job
from app.domain.notes.models import Note
from app.domain.notes.schema import NoteCreateUpdate

NOTE_TYPES = Literal["jobs", "interviews", "contacts"]
NOTE_MODELS = {
    "jobs": Job,
    "interviews": Interview,
    "contacts": Contact,
}


def create_note(
    db: Session,
    note_type: NOTE_TYPES,
    note_parent_id: int,
    note_create: NoteCreateUpdate,
) -> Note:
    """Create a new Note in DB"""
    parent = db.get(NOTE_MODELS[note_type], note_parent_id)
    if not parent:
        raise EntryNotFound

    try:
        note = Note(**note_create.model_dump())
        parent.notes.append(note)
        db.commit()
        return note
    except IntegrityError as e:
        db.rollback()
        raise EntryConflict from e


def read_note(db: Session, note_id: int) -> Note:
    """Read Interview from DB"""
    note = db.get(Note, note_id)
    return note


def read_notes(db: Session, note_type: NOTE_TYPES, note_parent_id: int) -> list[Note]:
    """Get Notes from DB"""
    parent = db.get(NOTE_MODELS[note_type], note_parent_id)
    if not parent:
        raise EntryNotFound
    return parent.notes


def update_note(
    db: Session,
    note_id: int,
    note_update: NoteCreateUpdate,
) -> Note:
    """Update existing Interview in DB"""
    note = db.get(Note, note_id)
    if not note:
        raise EntryNotFound
    try:
        update_data = note_update.model_dump()
        stmt = update(Note).where(Note.id == note_id).values(**update_data)
        db.execute(stmt)
        db.commit()
        return note
    except IntegrityError as e:
        db.rollback()
        raise EntryConflict from e
    except Exception as e:
        db.rollback()
        raise Exception from e


def delete_note(
    db: Session, note_type: NOTE_TYPES, note_parent_id: int, note_id: int
) -> None:
    """Delete existing Note from DB"""
    parent = db.get(NOTE_MODELS[note_type], note_parent_id)
    if not parent:
        raise EntryNotFound
    note = db.get(Note, note_id)
    if not note:
        raise EntryNotFound
    parent.notes.remove(note)
    db.delete(note)
    db.commit()
