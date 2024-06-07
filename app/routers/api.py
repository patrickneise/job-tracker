from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import EntryConflict, EntryNotFound, get_db

router = APIRouter(prefix="/api", tags=["api"])

#########################################
# Jobs
#########################################


@router.post("/jobs", status_code=status.HTTP_201_CREATED, response_model=schemas.Job)
def create_job_api(job_create: schemas.JobCreate, db: Session = Depends(get_db)):
    """Create a new Job"""
    db_job = crud.read_job_by_company_title(
        db=db, company=job_create.company, title=job_create.title
    )
    if db_job:
        raise HTTPException(status_code=400, detail="Job already exists")
    return crud.create_job(db=db, job_create=job_create)


@router.get("/jobs/{job_id}", response_model=schemas.Job)
def read_job_api(job_id: int, db: Session = Depends(get_db)):
    """Get a Job by ID"""
    db_job = crud.read_job(db=db, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job


@router.get("/jobs", response_model=list[schemas.Job])
def read_jobs_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    "Get all Jobs"
    jobs = crud.read_jobs(db=db, skip=skip, limit=limit)
    return jobs


@router.put(
    "/jobs/{job_id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Job
)
def update_job_api(
    job_id: int, job_update: schemas.JobUpdate, db: Session = Depends(get_db)
):
    """Update an existing Job"""
    try:
        updated_job = crud.update_job(db=db, job_id=job_id, job_update=job_update)
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


@router.delete("/jobs/{job_id}", status_code=status.HTTP_202_ACCEPTED)
def delete_job_api(job_id: int, db: Session = Depends(get_db)):
    """Delete an existing Job"""
    try:
        crud.delete_job(db=db, job_id=job_id)
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


#########################################
# Contacts
#########################################


@router.post(
    "/contacts",
    # "/jobs/{job_id}/contacts/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Contact,
)
def create_job_contact_api(
    job_id: int, contact_create: schemas.ContactCreate, db: Session = Depends(get_db)
):
    """Create a new Contact for a Job"""
    try:
        contact = crud.create_job_contact(
            db=db, job_id=job_id, contact_create=contact_create
        )
        return contact
    except EntryNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Job with this id: `{job_id}` found",
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the contact.",
        ) from e


@router.post("/contacts/{contact_id}", response_model=schemas.Job)
def add_job_contact_api(job_id: int, contact_id: int, db: Session = Depends(get_db)):
    """Add existing Contact to a Job"""
    try:
        job = crud.add_job_contact(db=db, job_id=job_id, contact_id=contact_id)
        return job
    except EntryNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Either Job.id or Contact.id does not exist",
        )
    except EntryConflict as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A Contact with the given details already exists on this Job.",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the job.",
        ) from e


@router.get("/contacts/{contact_id}", response_model=schemas.Contact)
def get_job_contact_api(job_id: int, contact_id: int, db: Session = Depends(get_db)):
    """Get a Contact by Job.id and Contact.id"""
    db_job_contact = crud.get_job_contact(db=db, job_id=job_id, contact_id=contact_id)
    if db_job_contact is None:
        raise HTTPException(
            status_code=404, detail=f"Contact not found for Job `{job_id}`"
        )
    return db_job_contact


@router.get("/contacts", response_model=list[schemas.Contact])
def get_job_contacts_api(job_id: int | None = None, db: Session = Depends(get_db)):
    """Get all Contacts by Job.id"""
    db_job_contacts = crud.get_job_contacts(db=db, job_id=job_id)
    return db_job_contacts


# Update Contact

# Delete Contact
