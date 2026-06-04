import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO
from core.dependancies.db.db import get_db
from core.dependancies.services.service_dependancy import get_application_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/pixel-auth-adapter/application", tags=["Application"])


@router.get(
    "/get-all",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Get all applications",
    description="Retrieve a list of all registered applications.",
)
async def get_all_applications(db: Session = Depends(get_db)) -> CommonResponseDTO:
    logger.info("application_router => get_all_applications function accessed")
    return get_application_service().get_all_applications(db)
