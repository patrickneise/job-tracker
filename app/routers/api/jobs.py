from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import jobs
from app.database import EntryConflict, EntryNotFound, get_db
from app.schemas.job import Job, JobCreate, JobUpdate

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Job)
def create_job_api(job_create: JobCreate, db: Session = Depends(get_db)):
    """Create a new Job"""
    db_job = jobs.read_job_by_company_title(
        db=db, company=job_create.company, title=job_create.title
    )
    if db_job:
        raise HTTPException(status_code=400, detail="Job already exists")
    return jobs.create_job(db=db, job_create=job_create)


@router.get("/{job_id}", response_model=Job)
def read_job_api(job_id: int, db: Session = Depends(get_db)):
    """Get a Job by ID"""
    db_job = jobs.read_job(db=db, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job


@router.get("", response_model=list[Job])
def read_jobs_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    "Get all Jobs"
    jobs = jobs.read_jobs(db=db, skip=skip, limit=limit)
    return jobs


@router.put("/{job_id}", status_code=status.HTTP_202_ACCEPTED, response_model=Job)
def update_job_api(job_id: int, job_update: JobUpdate, db: Session = Depends(get_db)):
    """Update an existing Job"""
    try:
        updated_job = jobs.update_job(db=db, job_id=job_id, job_update=job_update)
        return updated_job
    except EntryNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Job with this id: `{job_id}` found",
        )
    except EntryConflict as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A job with the given details already exists.",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the job.",
        ) from e


@router.delete("/{job_id}", status_code=status.HTTP_202_ACCEPTED)
def delete_job_api(job_id: int, db: Session = Depends(get_db)):
    """Delete an existing Job"""
    try:
        jobs.delete_job(db=db, job_id=job_id)
        return None
    except EntryNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Job with this id: `{job_id}` found",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the job.",
        ) from e