import logging
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO
from schemas.user_role_profile.user_role_profile_request import (
    UserRoleProfileRequestDTO,
)
from schemas.user_role_profile.user_role_profile_sync_request import (
    UserRoleProfileSyncRequestDTO,
)
from core.dependancies.db.db import get_db
from core.dependancies.services.service_dependancy import (
    get_user_role_profile_service,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/pixel-auth-adapter/user-role-profile",
    tags=["UserRoleProfile"],
)


@router.post(
    "/create",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create user role profile mappings (API & UI permissions)",
    description="Associate a realm, application, user role, list of modules, list of API permissions, and list of UI permissions.",
)
async def create_profile(
    req: UserRoleProfileRequestDTO, db: Session = Depends(get_db)
) -> CommonResponseDTO:
    logger.info("user_role_profile_router => create_profile: %s", req)
    return get_user_role_profile_service().create_profile(db, req)


@router.delete(
    "/delete/api",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Delete a user role API permission profile mapping by ID",
    description="Delete a mapping between realm, application, user role, module, and API permission by ID.",
)
async def delete_api_profile_by_id(
    mapping_id: int = Query(
        ..., description="The ID of the user role API profile mapping to delete"
    ),
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info("user_role_profile_router => delete_api_profile_by_id: %s", mapping_id)
    return get_user_role_profile_service().delete_api_profile_by_id(db, mapping_id)


@router.delete(
    "/delete/ui",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Delete a user role UI permission profile mapping by ID",
    description="Delete a mapping between realm, application, user role, module, and UI permission by ID.",
)
async def delete_ui_profile_by_id(
    mapping_id: int = Query(
        ..., description="The ID of the user role UI profile mapping to delete"
    ),
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info("user_role_profile_router => delete_ui_profile_by_id: %s", mapping_id)
    return get_user_role_profile_service().delete_ui_profile_by_id(db, mapping_id)


@router.get(
    "/search",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Search assigned user role profiles (API & UI)",
    description="Retrieve assigned user role API and UI permission profiles with optional filters.",
)
async def search_assigned_profiles(
    realm_id: int = Query(None, description="Optional realm ID filter"),
    application_id: int = Query(None, description="Optional application ID filter"),
    user_role_id: int = Query(None, description="Optional user role ID filter"),
    module_id: int = Query(None, description="Optional module ID filter"),
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info(
        "user_role_profile_router => search_assigned_profiles: realm_id=%s, application_id=%s, user_role_id=%s, module_id=%s",
        realm_id,
        application_id,
        user_role_id,
        module_id,
    )
    return get_user_role_profile_service().search_assigned_profiles(db, realm_id, application_id, user_role_id, module_id)


@router.post(
    "/sync",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Sync user role profile mappings",
    description="Synchronize a user role's module, API, and UI permission mappings.",
)
async def sync_profile(
    req: UserRoleProfileSyncRequestDTO, db: Session = Depends(get_db)
) -> CommonResponseDTO:
    logger.info("user_role_profile_router => sync_profile: %s", req)
    return get_user_role_profile_service().sync_profile(db, req)
