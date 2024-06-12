from fastapi import APIRouter

from .api_router import router as api_router

# from .app_router import router as app_router

router = APIRouter(prefix="", tags=["interviews"])
# /api/jobs/{job_id}/interviews
router.include_router(api_router)
# router.include_router(app_router)
