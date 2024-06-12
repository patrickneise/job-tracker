from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.database import EntryConflict, EntryNotFound, get_db
from app.domain.notes import crud
from app.domain.notes.schema import Note, NoteCreateUpdate


def get_note_type(request: Request) -> crud.NOTE_TYPES:
    path_parts = request.url.path.split("/")
    notes_index = path_parts.index("notes")
    parent_type = path_parts[notes_index - 2]
    return parent_type


router = APIRouter(prefix="/{note_parent_id}/notes")


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Note)
def create_note(
    note_parent_id: int,
    note_create: NoteCreateUpdate,
    note_type: crud.NOTE_TYPES = Depends(get_note_type),
    db: Session = Depends(get_db),
):
    """Create a new Note"""
    try:
        note = crud.create_note(
            db=db,
            note_type=note_type,
            note_parent_id=note_parent_id,
            note_create=note_create,
        )
        return note
    except EntryNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No {note_type.upper()} found.",
        )
    except EntryConflict as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An note with the given details already exists.",
        ) from e


@router.get("/{note_id}", response_model=Note)
def read_note(
    note_id: int,
    db: Session = Depends(get_db),
):
    """Get an Interview by ID"""
    note = crud.read_note(db=db, note_id=note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.get("", response_model=list[Note])
def read_notes(
    note_parent_id: int,
    note_type: crud.NOTE_TYPES = Depends(get_note_type),
    db: Session = Depends(get_db),
):
    "Get all Notes"
    notes = crud.read_notes(db=db, note_type=note_type, note_parent_id=note_parent_id)
    return notes


@router.put("/{note_id}", status_code=status.HTTP_202_ACCEPTED, response_model=Note)
def update_note(
    note_id: int,
    note_update: NoteCreateUpdate,
    db: Session = Depends(get_db),
):
    """Update an existing Note"""
    try:
        updated_note = crud.update_note(db=db, note_id=note_id, note_update=note_update)
        return updated_note
    except EntryNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Note with this id: `{note_id}` found",
        )
    except EntryConflict as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An Note with the given details already exists.",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the note.",
        ) from e


@router.delete("/{note_id}", status_code=status.HTTP_202_ACCEPTED)
def delete_note(
    note_parent_id: int,
    note_id: int,
    note_type: crud.NOTE_TYPES = Depends(get_note_type),
    db: Session = Depends(get_db),
):
    """Delete an existing Note"""
    try:
        crud.delete_note(
            db=db, note_type=note_type, note_parent_id=note_parent_id, note_id=note_id
        )
        return None
    except EntryNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Note with this id: `{note_id}` found",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the Note.",
        ) from e
