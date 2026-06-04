import logging

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO
from core.dependancies.db.db import get_db
from core.dependancies.services.service_dependancy import get_application_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/pixel-auth-adapter/application", tags=["Application"])


@router.post(
    "/search",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Search for applications",
    description="This endpoint allows you to search for applications based on provided criteria.",
)
async def search_applications(
    page: int = 0, size: int = 5, query: str = None, db: Session = Depends(get_db)
) -> CommonResponseDTO:

    logger.info(
        "application_router => search_applications function accessed: %s", query
    )

    return get_application_service().search_applications(db, page, size, query)
