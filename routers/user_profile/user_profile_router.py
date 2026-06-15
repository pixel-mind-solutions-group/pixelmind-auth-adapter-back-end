import logging
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO
from schemas.user_profile.user_profile_request import UserProfileRequestDTO
from core.dependancies.db.db import get_db
from core.dependancies.services.service_dependancy import get_user_profile_service

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/pixel-auth-adapter/user-profile",
    tags=["UserProfile"],
)


@router.post(
    "/register-or-modify",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new or modify an existing user profile mapping",
    description="Associate a user with a realm, application, and user role.",
)
async def register_modify_profile(
    req: UserProfileRequestDTO, db: Session = Depends(get_db)
) -> CommonResponseDTO:
    logger.info("user_profile_router => register_modify_profile: %s", req)
    return get_user_profile_service().create_or_update_profile(db, req)


@router.get(
    "/get",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Get user profile mapping by ID",
    description="Retrieve a single user profile mapping by its ID.",
)
async def get_profile_by_id(
    profile_id: int = Query(..., description="The ID of the user profile mapping to retrieve"),
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info("user_profile_router => get_profile_by_id: %s", profile_id)
    return get_user_profile_service().get_profile_by_id(db, profile_id)


@router.delete(
    "/delete",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Delete user profile mapping by ID",
    description="Delete a single user profile mapping by its ID.",
)
async def delete_profile_by_id(
    profile_id: int = Query(..., description="The ID of the user profile mapping to delete"),
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info("user_profile_router => delete_profile_by_id: %s", profile_id)
    return get_user_profile_service().delete_profile_by_id(db, profile_id)


@router.get(
    "/search",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Search user profiles with filtration",
    description="Search assigned user profiles with paging and filters.",
)
async def search_profiles(
    page: int = 0,
    size: int = 5,
    realm_id: int = Query(None, description="Optional realm ID filter"),
    application_id: int = Query(None, description="Optional application ID filter"),
    user_id: int = Query(None, description="Optional user ID filter"),
    user_role_id: int = Query(None, description="Optional user role ID filter"),
    query: str = Query(None, description="Optional general search query"),
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info(
        "user_profile_router => search_profiles: page=%s, size=%s, realm_id=%s, app_id=%s, user_id=%s, role_id=%s, query=%s",
        page,
        size,
        realm_id,
        application_id,
        user_id,
        user_role_id,
        query,
    )
    return get_user_profile_service().search_profiles(
        db, page, size, realm_id, application_id, user_id, user_role_id, query
    )
