from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import EntryConflict, EntryNotFound
from app.domain.jobs.models import Job
from app.domain.jobs.schema import JobCreate, JobUpdate


def create_job(db: Session, job_create: JobCreate) -> Job:
    """Create a new Job in DB"""
    try:
        job = Job(**job_create.model_dump())
        db.add(job)
        db.commit()
    except IntegrityError as e:
        raise EntryConflict from e
    return job


def read_job(db: Session, job_id: int) -> Job:
    """Get Job from DB"""
    job = db.get(Job, job_id)
    return job


def read_jobs(db: Session, skip: int = 0, limit: int = 100) -> list[Job]:
    """Get all Jobs from DB"""
    stmt = select(Job).offset(skip).limit(limit)
    jobs = db.execute(stmt).scalars().all()
    return jobs


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
        raise EntryConflict from e
    except Exception as e:
        raise Exception from e


def delete_job(db: Session, job_id: int) -> None:
    """Delete existing Job from DB"""
    job = db.get(Job, job_id)
    if not job:
        raise EntryNotFound
    db.delete(job)
    db.commit()
