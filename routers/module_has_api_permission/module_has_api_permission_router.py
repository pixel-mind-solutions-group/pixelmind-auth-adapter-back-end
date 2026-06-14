import logging
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO
from schemas.module_has_api_permission.module_has_api_permission_request import (
    ModuleHasApiPermissionRequestDTO,
)
from core.dependancies.db.db import get_db
from core.dependancies.services.service_dependancy import (
    get_module_has_api_permission_service,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/pixel-auth-adapter/module-has-api-permission",
    tags=["ModuleHasApiPermission"],
)


@router.post(
    "/create",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new module API permission mapping",
    description="Associate a module and permission.",
)
async def create_profile(
    req: ModuleHasApiPermissionRequestDTO, db: Session = Depends(get_db)
) -> CommonResponseDTO:
    logger.info(
        "module_has_api_permission_router => create_profile function accessed: %s",
        req,
    )
    return get_module_has_api_permission_service().create_profile(db, req)


@router.delete(
    "/delete",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Delete a module API permission mapping by ID",
    description="Delete a single module API permission mapping by its ID.",
)
async def delete_profile_by_id(
    module_has_api_permission_id: int = Query(
        ..., description="The ID of the permission mapping to delete"
    ),
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info(
        "module_has_api_permission_router => delete_profile_by_id function accessed: %s",
        module_has_api_permission_id,
    )
    return get_module_has_api_permission_service().delete_profile_by_id(
        db, module_has_api_permission_id
    )


@router.get(
    "/search",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Search assigned module API permissions",
    description="Retrieve list of assigned API permissions with optional filters.",
)
async def search_assigned_permissions(
    realm_id: int = Query(None, description="Optional realm ID to filter"),
    application_id: int = Query(None, description="Optional application ID to filter"),
    module_id: int = Query(None, description="Optional module ID to filter"),
    api_permission_name: str = Query(
        None, description="Optional API permission name to filter"
    ),
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info(
        "module_has_api_permission_router => search_assigned_permissions function accessed: realm_id=%s, application_id=%s, module_id=%s, api_permission_name=%s",
        realm_id,
        application_id,
        module_id,
        api_permission_name,
    )
    return get_module_has_api_permission_service().search_assigned_permissions(
        db, realm_id, application_id, module_id, api_permission_name
    )
