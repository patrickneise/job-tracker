from fastapi import APIRouter

from .api_router import router as api_router
from .api_router_contact import router as api_router_contact

# from .app_router import router as app_router

router = APIRouter(prefix="", tags=["contacts"])
# /api/jobs/{contact_parent_id}/contacts
router.include_router(api_router, prefix="/api/jobs", tags=["jobs"])
# /api/jobs/{job_id}/interviews/{contact_parent_id}/contacts
router.include_router(
    api_router, prefix="/jobs/{job_id}/interviews", tags=["interviews"]
)
router.include_router(api_router_contact)
# router.include_router(app_router)
