from fastapi import APIRouter

from app.routers.endpoints import jobs

router = APIRouter(prefix="", tags=["app"])
router.include_router(jobs.router)
