from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import EntryConflict, EntryNotFound
from app.domain.interviews.models import Interview
from app.domain.interviews.schema import InterviewCreate, InterviewUpdate
from app.domain.jobs.models import Job


def create_interview(
    db: Session, job_id: int, interview_create: InterviewCreate
) -> Interview:
    """Create a new Interview in DB"""
    job = db.get(Job, job_id)
    if not job:
        raise EntryNotFound
    try:
        interview = Interview(**interview_create.model_dump())
        job.interviews.append(interview)
        db.commit()
        return interview
    except IntegrityError as e:
        raise EntryConflict from e


def read_interview(db: Session, interview_id: int) -> Interview:
    """Read Interview from DB"""
    interview = db.get(Interview, interview_id)
    return interview


def read_interviews(
    db: Session, job_id: int, skip: int = 0, limit: int = 100
) -> list[Interview]:
    """Get Interviews from DB"""
    if job_id:
        job = db.get(Job, job_id)
        if not job:
            raise EntryNotFound
        interviews = job.interviews
    else:
        stmt = select(Interview).offset(skip).limit(limit)
        interviews = db.execute(stmt).scalars().all()
    return interviews


def update_interview(
    db: Session, interview_id: int, interview_update: InterviewUpdate
) -> Interview:
    """Update existing Interview in DB"""
    interview = db.get(Interview, interview_id)
    if not interview:
        raise EntryNotFound
    try:
        update_data = interview_update.model_dump(exclude_unset=True)
        stmt = (
            update(Interview).where(Interview.id == interview_id).values(**update_data)
        )
        db.execute(stmt)
        db.commit()
        db.refresh(interview)
        return interview
    except IntegrityError as e:
        raise EntryConflict from e
    except Exception as e:
        raise Exception from e


def delete_interview(db: Session, interview_id: int) -> None:
    """Delete existing Interview from DB"""
    interview = db.get(Interview, interview_id)
    if not interview:
        raise EntryNotFound
    db.delete(interview)
    db.commit()
