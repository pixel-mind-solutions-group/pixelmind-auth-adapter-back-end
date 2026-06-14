import logging
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO
from schemas.application_has_ui_permission.application_has_ui_permission_request import (
    ApplicationHasUiPermissionRequestDTO,
)
from core.dependancies.db.db import get_db
from core.dependancies.services.service_dependancy import (
    get_application_has_ui_permission_service,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/pixel-auth-adapter/application-has-ui-permission",
    tags=["ApplicationHasUiPermission"],
)


@router.post(
    "/create",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new application UI permission mapping",
    description="Associate a realm, application, and permission.",
)
async def create_profile(
    req: ApplicationHasUiPermissionRequestDTO, db: Session = Depends(get_db)
) -> CommonResponseDTO:
    logger.info(
        "application_has_ui_permission_router => create_profile function accessed: %s",
        req,
    )
    return get_application_has_ui_permission_service().create_profile(db, req)


@router.delete(
    "/delete",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Delete an application UI permission mapping by ID",
    description="Delete a single application UI permission mapping by its ID.",
)
async def delete_profile_by_id(
    application_has_ui_permission_id: int = Query(
        ..., description="The ID of the permission mapping to delete"
    ),
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info(
        "application_has_ui_permission_router => delete_profile_by_id function accessed: %s",
        application_has_ui_permission_id,
    )
    return get_application_has_ui_permission_service().delete_profile_by_id(
        db, application_has_ui_permission_id
    )


@router.get(
    "/search",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Search assigned UI permissions",
    description="Retrieve list of assigned UI permissions with optional filters.",
)
async def search_assigned_permissions(
    realm_id: int = Query(None, description="Optional realm ID to filter"),
    application_id: int = Query(None, description="Optional application ID to filter"),
    ui_permission_name: str = Query(
        None, description="Optional UI permission name to filter"
    ),
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info(
        "application_has_ui_permission_router => search_assigned_permissions function accessed: realm_id=%s, application_id=%s, ui_permission_name=%s",
        realm_id,
        application_id,
        ui_permission_name,
    )
    return get_application_has_ui_permission_service().search_assigned_permissions(
        db, realm_id, application_id, ui_permission_name
    )
