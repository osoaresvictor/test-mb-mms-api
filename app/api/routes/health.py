from fastapi import APIRouter

from app.services.health_service import perform_health_check

router = APIRouter()


@router.get("/health", tags=["Health"])
def health_check():
    return perform_health_check()
