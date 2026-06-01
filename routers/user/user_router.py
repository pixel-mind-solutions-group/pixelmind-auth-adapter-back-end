import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO
from schemas.user import user_request
from schemas.user.user_request import UserRequestDTO
from core.dependancies.db.db import get_db
from core.dependancies.services.service_dependancy import get_user_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/pixel-auth-adapter/user", tags=["User"])


@router.post(
    "/register-or-modify",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Register a new or modify an existing user",
    description="This endpoint allows you to register a new user or modify an existing user's information.",
)
async def register_modify_user(
    user_request: UserRequestDTO, db: Session = Depends(get_db)
) -> CommonResponseDTO:

    logger.info(
        "user_router => register_modify_user function accessed: %s", user_request
    )

    return get_user_service().create_or_update_user(db, user_request)


@router.get(
    "/search",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Search for a user list",
    description="This endpoint allows you to search for a user list based on provided criteria.",
)
async def search_users(
    page: int = 0, size: int = 5, query: str = None, db: Session = Depends(get_db)
) -> CommonResponseDTO:

    logger.info("user_router => search_users function accessed: %s", query)

    return get_user_service().search_users(db, page, size, query)
