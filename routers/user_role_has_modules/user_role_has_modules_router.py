import logging
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO
from schemas.user_role_has_modules.user_role_has_modules_request import (
    UserRoleHasModulesRequestDTO,
)
from core.dependancies.db.db import get_db
from core.dependancies.services.service_dependancy import (
    get_user_role_has_modules_service,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/pixel-auth-adapter/user-role-has-modules",
    tags=["UserRoleHasModules"],
)


@router.post(
    "/create",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create user role profile module mappings",
    description="Associate a realm, application, user role, and a list of modules.",
)
async def create_profile(
    req: UserRoleHasModulesRequestDTO, db: Session = Depends(get_db)
) -> CommonResponseDTO:
    logger.info("user_role_has_modules_router => create_profile: %s", req)
    return get_user_role_has_modules_service().create_profile(db, req)


@router.delete(
    "/delete",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Delete a user role module mapping by ID",
    description="Delete a mapping between realm, application, user role, and module by ID.",
)
async def delete_profile_by_id(
    user_role_has_modules_id: int = Query(
        ..., description="The ID of the role-module mapping to delete"
    ),
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info("user_role_has_modules_router => delete_profile_by_id: %s", user_role_has_modules_id)
    return get_user_role_has_modules_service().delete_profile_by_id(db, user_role_has_modules_id)


@router.get(
    "/search",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Search assigned user role profiles",
    description="Retrieve assigned user role module profiles with optional filters.",
)
async def search_assigned_profiles(
    realm_id: int = Query(None, description="Optional realm ID filter"),
    application_id: int = Query(None, description="Optional application ID filter"),
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info(
        "user_role_has_modules_router => search_assigned_profiles: realm_id=%s, application_id=%s",
        realm_id,
        application_id,
    )
    return get_user_role_has_modules_service().search_assigned_profiles(db, realm_id, application_id)
