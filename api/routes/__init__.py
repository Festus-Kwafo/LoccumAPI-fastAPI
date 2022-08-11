from fastapi import APIRouter
from api.routes.accounts import cleanings_router
from api.routes.job import job_router


router = APIRouter()

router.include_router(cleanings_router, prefix="/cleanings", tags=["cleanings"])
router.include_router(job_router, prefix="/job", tags=["job"])