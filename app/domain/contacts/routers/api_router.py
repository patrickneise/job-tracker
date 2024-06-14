from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.database import EntryConflict, EntryNotFound, get_db
from app.domain.contacts import crud
from app.domain.contacts.schema import Contact, ContactCreate, ContactUpdate


def get_contact_type(request: Request) -> crud.CONTACT_TYPES:
    path_parts = request.url.path.split("/")
    contacts_index = path_parts.index("contacts")
    parent_type = path_parts[contacts_index - 2]
    return parent_type


router = APIRouter(prefix="/{contact_parent_id}/contacts")


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=Contact,
)
def create_contact(
    contact_parent_id: int,
    contact_create: ContactCreate,
    contact_type: crud.CONTACT_TYPES = Depends(get_contact_type),
    db: Session = Depends(get_db),
):
    """Create a new Contact for a Job"""
    try:
        contact = crud.create_contact(
            db=db,
            contact_type=contact_type,
            contact_parent_id=contact_parent_id,
            contact_create=contact_create,
        )
        return contact
    except EntryNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No {contact_type.upper()} with this id: `{id}` found",
        )
    except EntryConflict:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A contact with those details already exists.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the contact.",
        ) from e


@router.get("/{contact_id}", response_model=Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = crud.read_contact(db=db, contact_id=contact_id)
    if not contact:
        raise HTTPException(
            status_code=404, detail=f"Contact not found for id `{contact_id}`"
        )
    return contact


@router.get("", response_model=list[Contact])
def read_contacts(
    contact_parent_id: int,
    contact_type: crud.CONTACT_TYPES = Depends(get_contact_type),
    db: Session = Depends(get_db),
):
    """Get all Contacts by Job.id"""
    contacts = crud.read_contacts(
        db=db, contact_type=contact_type, contact_parent_id=contact_parent_id
    )
    return contacts


@router.put(
    "/{contact_id}", status_code=status.HTTP_202_ACCEPTED, response_model=Contact
)
def update_contact(
    contact_id: int,
    contact_update: ContactUpdate,
    contact_parent_id: int,
    contact_type: crud.CONTACT_TYPES = Depends(get_contact_type),
    db: Session = Depends(get_db),
):
    """Update an existing Contact"""
    try:
        updated_contact = crud.update_contact(
            db=db,
            contact_id=contact_id,
            contact_update=contact_update,
            contact_parent_id=contact_parent_id,
            contact_type=contact_type,
        )
        return updated_contact
    except EntryNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Contact with this id: `{contact_id}` found",
        )
    except EntryConflict as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An Contact with the given details already exists.",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the Contact.",
        ) from e


@router.delete("/{contact_id}", status_code=status.HTTP_202_ACCEPTED)
def delete_contact(
    contact_parent_id: int,
    contact_id: int,
    contact_type: crud.CONTACT_TYPES = Depends(get_contact_type),
    db: Session = Depends(get_db),
):
    """Delete an existing Contact"""
    try:
        crud.remove_parent_contact(
            db=db,
            contact_type=contact_type,
            contact_parent_id=contact_parent_id,
            contact_id=contact_id,
        )
        return None
    except EntryNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Contact with this id: `{contact_id}` found",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the Contact.",
        ) from e
