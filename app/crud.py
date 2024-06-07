from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import models, schemas
from .database import EntryConflict, EntryNotFound

#########################################
# Jobs
#########################################


def create_job(db: Session, job_create: schemas.JobCreate) -> models.Job:
    """Create a new Job in DB"""
    job = models.Job(**job_create.model_dump())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def read_job(db: Session, job_id: int) -> models.Job:
    """Get Job from DB"""
    job = db.get(models.Job, job_id)
    return job


def read_jobs(db: Session, skip: int = 0, limit: int = 100) -> list[models.Job]:
    """Get all Jobs from DB"""
    stmt = select(models.Job).offset(skip).limit(limit)
    jobs = db.execute(stmt).scalars().all()
    return jobs


def read_job_by_company_title(db: Session, company: str, title: str) -> models.Job:
    """Get Job by `company` and `title`"""
    stmt = select(models.Job).filter(
        models.Job.company == company and models.Job.title == title
    )
    job = db.execute(stmt).scalar()
    return job


def update_job(db: Session, job_id: int, job_update: schemas.JobUpdate) -> models.Job:
    """Update existing Job in DB"""
    job = db.get(models.Job, job_id)
    if not job:
        raise EntryNotFound
    try:
        update_data = job_update.model_dump(exclude_unset=True)
        stmt = update(models.Job).where(models.Job.id == job_id).values(**update_data)
        db.execute(stmt)
        db.commit()
        db.refresh(job)
        return job
    except IntegrityError as e:
        db.rollback()
        raise EntryConflict from e
    except Exception as e:
        db.rollback()
        raise Exception from e


def delete_job(db: Session, job_id: int) -> None:
    """Delete existing Job from DB"""
    job = db.get(models.Job, job_id)
    if not job:
        raise EntryNotFound
    db.delete(job)
    db.commit()


#########################################
# Contacts
#########################################


def create_job_contact(
    db: Session, job_id: int, contact_create: schemas.ContactCreate
) -> models.Contact:
    """Create new Contact for Job"""
    job = db.get(models.Job, job_id)
    if not job:
        raise EntryNotFound

    contact = models.Contact(**contact_create.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)

    job.contacts.append(contact)
    db.commit()
    return contact


def add_job_contact(db: Session, job_id: int, contact_id: int) -> models.Job:
    """Add existing Contact to Job"""
    job = db.get(models.Job, job_id)
    if not job:
        raise EntryNotFound

    contact = db.get(models.Contact, contact_id)
    if not job:
        raise EntryNotFound

    try:
        job.contacts.append(contact)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise EntryConflict from e
    return job


# Get contact for job
# TODO: don't think this actually uses job_id
def get_job_contact(db: Session, job_id: int, contact_id: int) -> models.Contact:
    """Get Contact by Job.id and Contact.id"""
    stmt = select(models.Contact).where(
        models.Job.contacts.any(models.Contact.id == contact_id)
    )
    job_contact = db.execute(stmt).scalar_one_or_none()
    return job_contact


# Get all contacts for job
def get_job_contacts(db: Session, job_id: int) -> models.Contact:
    """Get all Contacts by Job.id"""
    if job_id:
        job = db.get(models.Job, job_id)
        contacts = job.contacts
    else:
        stmt = select(models.Contact)
        contacts = db.execute(stmt).scalars().all()
    return contacts
