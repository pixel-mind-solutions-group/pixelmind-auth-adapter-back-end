import logging
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO
from schemas.user_role.user_role_request import UserRoleRequestDTO
from core.dependancies.db.db import get_db
from core.dependancies.services.service_dependancy import get_user_role_service

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/pixel-auth-adapter/user-role",
    tags=["UserRole"],
)


@router.post(
    "/create-or-update",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create or update a user role",
    description="Create a new role or update an existing one if roleId is provided.",
)
async def create_or_update_role(
    req: UserRoleRequestDTO, db: Session = Depends(get_db)
) -> CommonResponseDTO:
    logger.info("user_role_router => create_or_update_role: %s", req)
    return get_user_role_service().create_or_update_role(db, req)


@router.get(
    "/get",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Get user role by ID",
    description="Retrieve detailed info about a role by its ID.",
)
async def get_role_by_id(
    role_id: int = Query(..., description="ID of the user role to fetch"),
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info("user_role_router => get_role_by_id: %s", role_id)
    return get_user_role_service().get_role_by_id(db, role_id)


@router.delete(
    "/delete",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Delete a user role by ID",
    description="Delete a user role from the database if not in use.",
)
async def delete_role_by_id(
    role_id: int = Query(..., description="ID of the user role to delete"),
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info("user_role_router => delete_role_by_id: %s", role_id)
    return get_user_role_service().delete_role_by_id(db, role_id)


@router.get(
    "/search",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Search user roles",
    description="Search user roles with pagination and optional filters.",
)
async def search_roles(
    page: int = Query(0, description="Page number (0-indexed)"),
    size: int = Query(10, description="Page size"),
    query: str = Query(None, description="Search term for role name or description"),
    active: bool = Query(None, description="Active status filter"),
    realm_id: int = Query(None, description="Realm ID to filter roles"),
    application_id: int = Query(None, description="Application ID to filter roles"),
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info(
        "user_role_router => search_roles: page=%s, size=%s, query=%s, active=%s, realm_id=%s, application_id=%s",
        page,
        size,
        query,
        active,
        realm_id,
        application_id,
    )
    return get_user_role_service().search_roles(
        db, page, size, query, active, realm_id, application_id
    )


@router.get(
    "/active",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Get all active user roles",
    description="Retrieve a list of active roles optionally filtered by realm and application.",
)
async def get_all_active_roles(
    realm_id: int = Query(None, description="Realm ID to filter active roles"),
    application_id: int = Query(None, description="Application ID to filter active roles"),
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info("user_role_router => get_all_active_roles: realm_id=%s, application_id=%s", realm_id, application_id)
    return get_user_role_service().get_all_active_roles(db, realm_id, application_id)

