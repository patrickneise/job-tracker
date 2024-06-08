from fastapi import APIRouter

from app.routers.api import contacts, jobs

router = APIRouter(prefix="/api", tags=["api"])
router.include_router(jobs.router)
router.include_router(contacts.router)
