import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO
from schemas.auth.auth_request import TokenRequestDTO
from core.dependancies.db.db import get_db
from core.dependancies.services.service_dependancy import get_auth_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/pixel-auth-adapter/auth", tags=["Auth"])


@router.post(
    "/token",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Get access and refresh tokens",
    description="Pass username, password and application_uuid to fetch user tokens from Keycloak.",
)
async def get_token(
    request: TokenRequestDTO, db: Session = Depends(get_db)
) -> CommonResponseDTO:

    logger.info(
        "auth_router => get_token function accessed: username=%s, application_uuid=%s",
        request.username,
        request.application_uuid,
    )

    return get_auth_service().get_token(db, request)
