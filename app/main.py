from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import engine
from app.models.base import Base
from app.routers import api, endpoints

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory=Path("app") / "static"), name="static")


app.include_router(api.router)
app.include_router(endpoints.router)
templates = Jinja2Templates(directory=Path("app") / "templates")


@app.get("/", response_class=HTMLResponse)
def get_index(request: Request):
    return templates.TemplateResponse(request, "index.html")
