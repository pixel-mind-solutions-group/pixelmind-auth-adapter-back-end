import logging
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO
from schemas.application_has_api_permission.application_has_api_permission_request import (
    ApplicationHasApiPermissionRequestDTO,
)
from core.dependancies.db.db import get_db
from core.dependancies.services.service_dependancy import (
    get_application_has_api_permission_service,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/pixel-auth-adapter/application-has-api-permission",
    tags=["ApplicationHasApiPermission"],
)


@router.post(
    "/create",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new application API permission mapping",
    description="Associate a realm, application, and permission.",
)
async def create_profile(
    req: ApplicationHasApiPermissionRequestDTO, db: Session = Depends(get_db)
) -> CommonResponseDTO:
    logger.info(
        "application_has_api_permission_router => create_profile function accessed: %s",
        req,
    )
    return get_application_has_api_permission_service().create_profile(db, req)


@router.delete(
    "/delete",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Delete an application API permission mapping by ID",
    description="Delete a single application API permission mapping by its ID.",
)
async def delete_profile_by_id(
    application_has_api_permission_id: int = Query(
        ..., description="The ID of the permission mapping to delete"
    ),
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info(
        "application_has_api_permission_router => delete_profile_by_id function accessed: %s",
        application_has_api_permission_id,
    )
    return get_application_has_api_permission_service().delete_profile_by_id(
        db, application_has_api_permission_id
    )
