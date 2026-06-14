import logging
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO
from schemas.module_has_ui_permission.module_has_ui_permission_request import (
    ModuleHasUiPermissionRequestDTO,
)
from core.dependancies.db.db import get_db
from core.dependancies.services.service_dependancy import (
    get_module_has_ui_permission_service,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/pixel-auth-adapter/module-has-ui-permission",
    tags=["ModuleHasUiPermission"],
)


@router.post(
    "/create",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new module UI permission mapping",
    description="Associate a module and permission.",
)
async def create_profile(
    req: ModuleHasUiPermissionRequestDTO, db: Session = Depends(get_db)
) -> CommonResponseDTO:
    logger.info(
        "module_has_ui_permission_router => create_profile function accessed: %s",
        req,
    )
    return get_module_has_ui_permission_service().create_profile(db, req)


@router.delete(
    "/delete",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Delete a module UI permission mapping by ID",
    description="Delete a single module UI permission mapping by its ID.",
)
async def delete_profile_by_id(
    module_has_ui_permission_id: int = Query(
        ..., description="The ID of the permission mapping to delete"
    ),
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info(
        "module_has_ui_permission_router => delete_profile_by_id function accessed: %s",
        module_has_ui_permission_id,
    )
    return get_module_has_ui_permission_service().delete_profile_by_id(
        db, module_has_ui_permission_id
    )


@router.get(
    "/search",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Search assigned module UI permissions",
    description="Retrieve list of assigned UI permissions with optional filters.",
)
async def search_assigned_permissions(
    realm_id: int = Query(None, description="Optional realm ID to filter"),
    application_id: int = Query(None, description="Optional application ID to filter"),
    module_id: int = Query(None, description="Optional module ID to filter"),
    query: str = Query(None, description="Optional query string to filter"),
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info(
        "module_has_ui_permission_router => search_assigned_permissions function accessed: realm_id=%s, application_id=%s, module_id=%s, query=%s",
        realm_id,
        application_id,
        module_id,
        query,
    )
    return get_module_has_ui_permission_service().search_assigned_permissions(
        db, realm_id, application_id, module_id, query
    )
