from typing import Literal

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import EntryConflict, EntryNotFound
from app.domain.contacts.models import Contact
from app.domain.contacts.schema import ContactCreate, ContactUpdate
from app.domain.interviews.models import Interview
from app.domain.jobs.models import Job

CONTACT_TYPES = Literal["jobs", "interviews"]
CONTACT_MODELS = {
    "jobs": Job,
    "interviews": Interview,
}


# TODO: separate "add contact" and "create contact"?
def create_contact(
    db: Session,
    contact_create: ContactCreate,
    contact_type: CONTACT_TYPES = None,
    contact_parent_id: int = None,
) -> Contact:
    """Create new Contact"""
    try:
        contact = Contact(**contact_create.model_dump())
        db.add(contact)
        if contact_type:
            parent = db.get(CONTACT_MODELS[contact_type], contact_parent_id)
            if not parent:
                raise EntryNotFound
            parent.contacts.append(contact)
        db.commit()
        db.refresh(contact)
        return contact
    except IntegrityError as e:
        db.rollback()
        raise EntryConflict from e
    except Exception as e:
        db.rollback()
        raise Exception from e


def read_contact(db: Session, contact_id: int) -> Contact:
    """Get Contact"""
    contact = db.get(Contact, contact_id)
    return contact


def read_contacts(
    db: Session, contact_type: CONTACT_TYPES = None, contact_parent_id: int = None
) -> Contact:
    """Get all Contacts"""
    if contact_type:
        parent = db.get(CONTACT_MODELS[contact_type], contact_parent_id)
        if not parent:
            raise EntryNotFound
        contacts = parent.contacts
    else:
        stmt = select(Contact)
        contacts = db.execute(stmt).scalars().all()
    return contacts


def update_contact(
    db: Session,
    contact_id: int,
    contact_update: ContactUpdate,
    contact_type: CONTACT_TYPES = None,
    contact_parent_id: int = None,
) -> Job:
    """Update existing Job in DB"""
    contact = db.get(Contact, contact_id)
    if not contact:
        raise EntryNotFound
    try:
        update_data = contact_update.model_dump(exclude_unset=True)
        stmt = update(Contact).where(Contact.id == contact_id).values(**update_data)
        db.execute(stmt)
        db.commit()
        db.refresh(contact)
        if contact_type:
            parent = db.get(CONTACT_MODELS[contact_type], contact_parent_id)
            if not parent:
                raise EntryNotFound
            parent.contacts.append(contact)
            db.commit()
        return contact
    except IntegrityError as e:
        db.rollback()
        raise EntryConflict from e
    except Exception as e:
        db.rollback()
        raise Exception from e


# TODO: separate "remove contact" and "delete contact"?
def remove_parent_contact(
    db: Session, contact_type: CONTACT_TYPES, contact_parent_id: int, contact_id: int
) -> None:
    """Delete existing Job from DB"""
    parent = db.get(CONTACT_MODELS[contact_type], contact_parent_id)

    if not parent:
        raise EntryNotFound

    contact = db.get(Contact, contact_id)
    if not contact:
        raise EntryNotFound

    parent.contacts.remove(contact)

    db.commit()


def delete_contact(db: Session, contact_id: int) -> None:
    """Delete existing Job from DB"""
    contact = db.get(Contact, contact_id)
    if not contact:
        raise EntryNotFound

    contact.jobs.clear()
    contact.interviews.clear()
    db.delete(contact)
    db.commit()
