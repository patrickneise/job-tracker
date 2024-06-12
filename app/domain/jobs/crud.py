from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import EntryConflict, EntryNotFound
from app.domain.jobs.models import Job
from app.domain.jobs.schema import JobCreate, JobUpdate


def create_job(db: Session, job_create: JobCreate) -> Job:
    """Create a new Job in DB"""
    job = Job(**job_create.model_dump())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def read_job(db: Session, job_id: int) -> Job:
    """Get Job from DB"""
    job = db.get(Job, job_id)
    if not job:
        raise EntryNotFound
    return job


# TODO: add optional query filter for status?
def read_jobs(db: Session, skip: int = 0, limit: int = 100) -> list[Job]:
    """Get all Jobs from DB"""
    stmt = select(Job).offset(skip).limit(limit)
    jobs = db.execute(stmt).scalars().all()
    return jobs


def read_job_by_company_title(db: Session, company: str, title: str) -> Job:
    """Get Job by `company` and `title`"""
    stmt = select(Job).filter(Job.company == company and Job.title == title)
    job = db.execute(stmt).scalar()
    return job


def update_job(db: Session, job_id: int, job_update: JobUpdate) -> Job:
    """Update existing Job in DB"""
    job = db.get(Job, job_id)
    if not job:
        raise EntryNotFound
    try:
        update_data = job_update.model_dump(exclude_unset=True)
        stmt = update(Job).where(Job.id == job_id).values(**update_data)
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
    job = db.get(Job, job_id)
    if not job:
        raise EntryNotFound
    db.delete(job)
    db.commit()
