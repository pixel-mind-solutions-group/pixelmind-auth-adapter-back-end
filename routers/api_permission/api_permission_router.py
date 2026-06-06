import logging
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO
from schemas.api_permission.api_permission_request import ApiPermissionRequestDTO
from core.dependancies.db.db import get_db
from core.dependancies.services.service_dependancy import get_api_permission_service

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/pixel-auth-adapter/api-permission", tags=["ApiPermission"]
)


@router.post(
    "/create-or-update",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Create a new or update an existing permission",
    description="Create or update an API permission.",
)
async def create_or_update_permission(
    req: ApiPermissionRequestDTO, db: Session = Depends(get_db)
) -> CommonResponseDTO:
    logger.info(
        "api_permission_router => create_or_update_permission function accessed: %s",
        req,
    )
    return get_api_permission_service().create_or_update_permission(db, req)


@router.get(
    "/search",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Search permissions",
    description="Search for API permissions with filters.",
)
async def search_permissions(
    page: int = 0,
    size: int = 5,
    query: str = None,
    active: bool = None,
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info(
        "api_permission_router => search_permissions function accessed: query=%s, active=%s",
        query,
        active,
    )
    return get_api_permission_service().search_permissions(
        db, page, size, query, active
    )


@router.get(
    "/active",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Get all active permissions",
    description="Retrieve list of all active permissions.",
)
async def get_all_active_permissions(
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info("api_permission_router => get_all_active_permissions function accessed")
    return get_api_permission_service().get_all_active_permissions(db)


@router.get(
    "/get",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Get a permission by ID",
    description="Retrieve a single API permission by its ID.",
)
async def get_permission_by_id(
    api_permission_id: int = Query(
        ..., description="The ID of the permission to retrieve"
    ),
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info(
        "api_permission_router => get_permission_by_id function accessed: %s",
        api_permission_id,
    )
    return get_api_permission_service().get_permission_by_id(db, api_permission_id)


@router.delete(
    "/delete",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Delete a permission by ID",
    description="Delete a single API permission by its ID.",
)
async def delete_permission_by_id(
    api_permission_id: int = Query(
        ..., description="The ID of the permission to delete"
    ),
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info(
        "api_permission_router => delete_permission_by_id function accessed: %s",
        api_permission_id,
    )
    return get_api_permission_service().delete_permission_by_id(db, api_permission_id)
