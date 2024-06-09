from pathlib import Path
from typing import get_args

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import EntryConflict, EntryNotFound, get_db
from app.jobs import crud
from app.jobs.schema import JobCreate, JobUpdate
from app.models import Status

STATUSES = list(get_args(Status))

router = APIRouter(prefix="/jobs", tags=["jobs", "app"])
templates = Jinja2Templates(directory=Path("app") / "templates")


@router.get("/create", response_class=HTMLResponse)
def get_create_job_form(request: Request):
    return templates.TemplateResponse(
        request, "create_job.html", {"statuses": STATUSES}
    )


@router.post("", response_class=HTMLResponse)
def create_job(
    request: Request,
    job_create: JobCreate = Depends(JobCreate.as_form),
    db: Session = Depends(get_db),
):
    db_job = crud.read_job_by_company_title(
        db=db, company=job_create.company, title=job_create.title
    )
    if db_job:
        raise HTTPException(status_code=400, detail="Job already exists")
    created_job = crud.create_job(db=db, job_create=job_create)
    return templates.TemplateResponse(
        request,
        "view_job.html",
        {"job": created_job},
        headers={"HX-Push-Url": f"/jobs/{created_job.id}"},
    )


@router.get("/{job_id}", response_class=HTMLResponse)
def get_job(request: Request, job_id: int, db: Session = Depends(get_db)):
    job = crud.read_job(db=db, job_id=job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return templates.TemplateResponse(request, "view_job.html", {"job": job})


@router.get("", response_class=HTMLResponse)
def get_jobs(
    request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    db_jobs = crud.read_jobs(db=db, skip=skip, limit=limit)
    status_counts = {}
    for status_name in STATUSES:
        status_counts[status_name] = sum(
            [True for job in db_jobs if job.status == status_name]
        )
    print(status_counts)
    return templates.TemplateResponse(
        request, "view_jobs.html", {"jobs": db_jobs, "status_counts": status_counts}
    )


@router.get("/{job_id}/edit", response_class=HTMLResponse)
def get_edit_job_form(request: Request, job_id: int, db: Session = Depends(get_db)):
    job = crud.read_job(db=db, job_id=job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return templates.TemplateResponse(
        request,
        "edit_job.html",
        {"job": job, "statuses": STATUSES},
    )


@router.put("/{job_id}", response_class=HTMLResponse)
def update_job(
    request: Request,
    job_id: int,
    job_update: JobUpdate = Depends(JobUpdate.as_form),
    db: Session = Depends(get_db),
):
    try:
        updated_job = crud.update_job(db=db, job_id=job_id, job_update=job_update)
        return templates.TemplateResponse(
            request, "view_job.html", {"job": updated_job}
        )
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


@router.delete("/{job_id}")
def delete_job(request: Request, job_id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_job(db=db, job_id=job_id)
        if request.headers["hx-current-url"].endswith("jobs"):
            return Response(status_code=status.HTTP_200_OK)
        else:
            return RedirectResponse(
                request.url_for("read_jobs"),
                status_code=status.HTTP_303_SEE_OTHER,
                headers={"HX-Push-Url": "/jobs"},
            )
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
