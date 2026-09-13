import logging
from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO
from schemas.auth.auth_request import TokenRequestDTO
from core.dependancies.db.db import get_db
from core.dependancies.services.service_dependancy import get_auth_service
from core.dependancies.security.auth_dependency import get_token_from_header

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


@router.get(
    "/user-details",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Get authenticated user details, role, and UI permissions (componentList)",
    description="Verifies the Bearer access token through Keycloak, authorizes the user, and returns user details with componentList.",
)
async def get_user_details(
    token: str = Depends(get_token_from_header),
    application_uuid: Optional[str] = Query(
        None,
        description="Optional application UUID to scope role and UI permissions (defaults to token claims if omitted)",
    ),
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info(
        "auth_router => get_user_details function accessed with application_uuid=%s",
        application_uuid,
    )
    return get_auth_service().get_user_details(
        db=db, token=token, application_uuid=application_uuid
    )
