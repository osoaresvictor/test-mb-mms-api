from fastapi import APIRouter

from app.api.routes.health import router as health_router
from app.api.routes.mms import router as mms_router

router = APIRouter()
router.include_router(mms_router)
router.include_router(health_router)
