from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import engine
from app.domain.contacts import routers as contacts_router
from app.domain.interviews import routers as interviews_router
from app.domain.jobs import routers as jobs_router
from app.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory=Path("app") / "static"), name="static")

app.include_router(contacts_router.router)
app.include_router(interviews_router.router)
app.include_router(jobs_router.router)

templates = Jinja2Templates(directory=Path("app") / "templates")


@app.get("/", response_class=HTMLResponse)
def get_index(request: Request):
    return templates.TemplateResponse(request, "index.html")
