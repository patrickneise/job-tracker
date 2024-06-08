from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.contacts import crud
from app.contacts.schema import Contact, ContactCreate
from app.database import EntryNotFound, get_db

router = APIRouter(prefix="/api/contacts", tags=["contacts"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=Contact,
)
def create_contact_api(
    contact_type: crud.CONTACT_TYPES,
    contact_create: ContactCreate,
    id: int,
    db: Session = Depends(get_db),
):
    """Create a new Contact for a Job"""
    try:
        if contact_type == "job":
            contact = crud.create_contact(
                db=db, contact_type=contact_type, id=id, contact_create=contact_create
            )
            return contact
        # TODO: handle creation for interview -> likely move contact_type evaulation to crud function
    except EntryNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No {contact_type.upper()} with this id: `{id}` found",
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the contact.",
        ) from e


@router.get("/{contact_id}", response_model=Contact)
def get_job_contact_api(job_id: int, contact_id: int, db: Session = Depends(get_db)):
    """Get a Contact by Job.id and Contact.id"""
    db_job_contact = crud.get_job_contact(db=db, job_id=job_id, contact_id=contact_id)
    if db_job_contact is None:
        raise HTTPException(
            status_code=404, detail=f"Contact not found for Job `{job_id}`"
        )
    return db_job_contact


@router.get("", response_model=list[Contact])
def get_job_contacts_api(
    contact_type: crud.CONTACT_TYPES | None = None,
    id: int | None = None,
    db: Session = Depends(get_db),
):
    """Get all Contacts by Job.id"""
    db_job_contacts = crud.get_job_contacts(db=db, contact_type=contact_type, id=id)
    return db_job_contacts
