from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from app.api.routes.health import router as health_router
from app.api.routes.mms import router as mms_router

router = APIRouter()
router.include_router(mms_router)
router.include_router(health_router)


@router.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")
