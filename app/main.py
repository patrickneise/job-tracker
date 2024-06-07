from pathlib import Path
from typing import get_args

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import EntryConflict, EntryNotFound, engine, get_db
from .routers import api

STATUSES = list(get_args(models.Status))


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory=Path("app") / "static"), name="static")
app.include_router(api.router)
templates = Jinja2Templates(directory=Path("app") / "templates")


@app.get("/", response_class=HTMLResponse)
def get_index(request: Request):
    return templates.TemplateResponse(request, "index.html")


#########################################
# Jobs
#########################################


# Create
@app.get("/jobs/create", response_class=HTMLResponse)
def get_create_job_form(request: Request):
    return templates.TemplateResponse(
        request, "create_job.html", {"statuses": STATUSES}
    )


@app.post("/jobs", response_class=HTMLResponse)
def create_job(
    request: Request,
    job_create: schemas.JobCreate = Depends(schemas.JobCreate.as_form),
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


# Read
@app.get("/jobs/{job_id}", response_class=HTMLResponse)
def get_job(request: Request, job_id: int, db: Session = Depends(get_db)):
    job = crud.read_job(db=db, job_id=job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return templates.TemplateResponse(request, "view_job.html", {"job": job})


@app.get("/jobs", response_class=HTMLResponse)
def get_jobs(
    request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    jobs = crud.read_jobs(db=db, skip=skip, limit=limit)
    return templates.TemplateResponse(
        request, "view_jobs.html", {"jobs": jobs, "statuses": STATUSES}
    )


# Update
@app.get("/jobs/{job_id}/edit", response_class=HTMLResponse)
def get_edit_job_form(request: Request, job_id: int, db: Session = Depends(get_db)):
    job = crud.read_job(db=db, job_id=job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return templates.TemplateResponse(
        request,
        "edit_job.html",
        {"job": job, "statuses": STATUSES},
    )


@app.put("/jobs/{job_id}", response_class=HTMLResponse)
def update_job(
    request: Request,
    job_id: int,
    job_update: schemas.JobUpdate = Depends(schemas.JobUpdate.as_form),
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


# Delete
@app.delete("/jobs/{job_id}")
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


#########################################
# Contacts
#########################################


# Create

# Get Contact by ID

# Get Contacts

# Update Contact

# Delete Contact
