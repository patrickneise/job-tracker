from typing import Literal

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import EntryConflict, EntryNotFound
from app.models.contact import Contact
from app.models.interview import Interview
from app.models.job import Job
from app.schemas.contact import ContactCreate, ContactUpdate

CONTACT_TYPES = Literal["job", "interview"]


def create_contact(
    db: Session, contact_type: CONTACT_TYPES, id: int, contact_create: ContactCreate
) -> Contact:
    """Create new Contact"""
    if contact_type == "job":
        parent_model = Job
    elif contact_type == "interview":
        parent_model = Interview

    parent = db.get(parent_model, id)
    if not parent:
        raise EntryNotFound

    # TODO: deicde how to handle existing contact
    stmt = select(Contact).where(Contact.email == contact_create.email)
    contact = db.execute(stmt).scalar_one_or_none()
    if not contact:
        contact = Contact(**contact_create.model_dump())
        db.add(contact)
        db.commit()
        db.refresh(contact)

    parent.contacts.append(contact)
    db.commit()
    return contact


def read_contact(db: Session, contact_id: int) -> Contact:
    """Get Contact"""
    contact = db.get(Contact, contact_id)
    return contact


def read_contacts(db: Session, contact_type: CONTACT_TYPES, id: int) -> Contact:
    """Get all Contacts"""
    if contact_type == "job":
        parent_model = Job
    elif contact_type == "interview":
        parent_model = Interview

    if id:
        parent = db.get(parent_model, id)
        contacts = parent.contacts
    else:
        stmt = select(Contact)
        contacts = db.execute(stmt).scalars().all()
    return contacts


def update_contact(db: Session, contact_id: int, contact_update: ContactUpdate) -> Job:
    """Update existing Job in DB"""
    contact = db.get(Contact, contact_id)
    if not contact:
        raise EntryNotFound
    try:
        update_data = contact_update.model_dump(exclude_unset=True)
        stmt = update(Job).where(Job.id == contact_update.id).values(**update_data)
        db.execute(stmt)
        db.commit()
        db.refresh(contact)
        return contact
    except IntegrityError as e:
        db.rollback()
        raise EntryConflict from e
    except Exception as e:
        db.rollback()
        raise Exception from e


def delete_contact(db: Session, contact_id: int) -> None:
    """Delete existing Job from DB"""
    contact = db.get(Contact, contact_id)
    if not contact:
        raise EntryNotFound
    db.delete(contact)
    db.commit()
