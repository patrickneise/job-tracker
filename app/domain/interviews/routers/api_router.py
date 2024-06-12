from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import EntryConflict, EntryNotFound, get_db
from app.domain.interviews import crud
from app.domain.interviews.schema import Interview, InterviewCreate, InterviewUpdate

router = APIRouter(prefix="/api/jobs/{job_id}/interviews")


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Interview)
def create_interview(
    job_id: int, interview_create: InterviewCreate, db: Session = Depends(get_db)
):
    """Create a new Interview"""
    try:
        interview = crud.create_interview(
            db=db, job_id=job_id, interview_create=interview_create
        )
        return interview
    except EntryConflict as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An interview with the given details already exists.",
        ) from e


@router.get("/{interview_id}", response_model=Interview)
def read_interview(interview_id: int, db: Session = Depends(get_db)):
    """Get an Interview by ID"""
    interview = crud.read_interview(db=db, interview_id=interview_id)
    if interview is None:
        raise HTTPException(status_code=404, detail="Interview not found")
    return interview


@router.get("", response_model=list[Interview])
def read_interviews(
    job_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    "Get all Interviews"
    try:
        interviews = crud.read_interviews(db=db, job_id=job_id, skip=skip, limit=limit)
        return interviews
    except EntryNotFound:
        raise HTTPException(status_code=404, detail="Job not found")


@router.put(
    "/{interview_id}", status_code=status.HTTP_202_ACCEPTED, response_model=Interview
)
def update_interview(
    interview_id: int, interview_update: InterviewUpdate, db: Session = Depends(get_db)
):
    """Update an existing Interview"""
    try:
        updated_interview = crud.update_interview(
            db=db, interview_id=interview_id, interview_update=interview_update
        )
        return updated_interview
    except EntryNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Interview with this id: `{interview_id}` found",
        )
    except EntryConflict as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An interview with the given details already exists.",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the interivew.",
        ) from e


@router.delete("/{interview_id}", status_code=status.HTTP_202_ACCEPTED)
def delete_interview(interview_id: int, db: Session = Depends(get_db)):
    """Delete an existing Interview"""
    try:
        crud.delete_interview(db=db, interview_id=interview_id)
        return None
    except EntryNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Interview with this id: `{interview_id}` found",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the interview.",
        ) from e
