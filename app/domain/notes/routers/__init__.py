from fastapi import APIRouter

from .api_router import router as api_router

# from .app_router import router as app_router

router = APIRouter(prefix="", tags=["notes"])
# /api/jobs/{note_parent_id}/notes
router.include_router(api_router, prefix="/api/jobs", tags=["jobs"])
# /api/jobs/{job_id}/interviews/{note_parent_id}/notes
router.include_router(
    api_router, prefix="/api/jobs/{job_id}/interviews", tags=["interviews"]
)
# /api/jobs/{job_id}/contacts/{note_parent_id}/notes
router.include_router(
    api_router, prefix="/api/jobs/{job_id}/contacts", tags=["contacts"]
)
# /api/jobs/{job_id}/interviews/{interview_id}/contacts/{note_parent_id}/notes
router.include_router(
    api_router,
    prefix="/api/jobs/{job_id}/interviews/{interview_id}/contacts",
    tags=["contacts"],
)

# router.include_router(app_router)
