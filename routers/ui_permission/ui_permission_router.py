import logging
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO
from schemas.ui_permission.ui_permission_request import UiPermissionRequestDTO
from core.dependancies.db.db import get_db
from core.dependancies.services.service_dependancy import get_ui_permission_service

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/pixel-auth-adapter/ui-permission", tags=["UiPermission"]
)


@router.post(
    "/create-or-update",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Create a new or update an existing permission",
    description="Create or update a UI permission.",
)
async def create_or_update_permission(
    req: UiPermissionRequestDTO, db: Session = Depends(get_db)
) -> CommonResponseDTO:
    logger.info(
        "ui_permission_router => create_or_update_permission function accessed: %s",
        req,
    )
    return get_ui_permission_service().create_or_update_permission(db, req)


@router.get(
    "/search",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Search permissions",
    description="Search for UI permissions with filters.",
)
async def search_permissions(
    page: int = 0,
    size: int = 5,
    query: str = None,
    active: bool = None,
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info(
        "ui_permission_router => search_permissions function accessed: query=%s, active=%s",
        query,
        active,
    )
    return get_ui_permission_service().search_permissions(db, page, size, query, active)


@router.get(
    "/active",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Get all active permissions",
    description="Retrieve list of all active permissions.",
)
async def get_all_active_permissions(
    realm_id: int = Query(..., description="The realm ID"),
    application_id: int = Query(..., description="The application ID"),
    ui_permission_name: str = Query(
        None, description="Optional UI permission name to retrieve"
    ),
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info(
        "ui_permission_router => get_all_active_permissions function accessed: realm_id=%s, application_id=%s, ui_permission_name=%s",
        realm_id,
        application_id,
        ui_permission_name,
    )
    return get_ui_permission_service().get_all_active_permissions(
        db, realm_id, application_id, ui_permission_name
    )


@router.get(
    "/get",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Get a permission by ID",
    description="Retrieve a single UI permission by its ID.",
)
async def get_permission_by_id(
    ui_permission_id: int = Query(
        ..., description="The ID of the permission to retrieve"
    ),
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info(
        "ui_permission_router => get_permission_by_id function accessed: %s",
        ui_permission_id,
    )
    return get_ui_permission_service().get_permission_by_id(db, ui_permission_id)


@router.delete(
    "/delete",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Delete a permission by ID",
    description="Delete a single UI permission by its ID.",
)
async def delete_permission_by_id(
    ui_permission_id: int = Query(
        ..., description="The ID of the permission to delete"
    ),
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info(
        "ui_permission_router => delete_permission_by_id function accessed: %s",
        ui_permission_id,
    )
    return get_ui_permission_service().delete_permission_by_id(db, ui_permission_id)
