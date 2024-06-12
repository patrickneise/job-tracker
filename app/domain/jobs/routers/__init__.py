from fastapi import APIRouter

from .api_router import router as api_router
from .app_router import router as app_router

router = APIRouter(prefix="", tags=["jobs"])
# /api/jobs
router.include_router(api_router)
# /jobs
router.include_router(app_router, tags=["app"])
