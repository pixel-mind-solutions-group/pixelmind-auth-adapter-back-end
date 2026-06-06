import logging
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO
from schemas.module.module_request import ModuleRequestDTO
from core.dependancies.db.db import get_db
from core.dependancies.services.service_dependancy import get_module_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/pixel-auth-adapter/module", tags=["Module"])


@router.post(
    "/create-or-update",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Create a new or update an existing module",
    description="This endpoint allows you to create a new module or update an existing one.",
)
async def create_or_update_module(
    module_request: ModuleRequestDTO, db: Session = Depends(get_db)
) -> CommonResponseDTO:
    logger.info(
        "module_router => create_or_update_module function accessed: %s", module_request
    )
    return get_module_service().create_or_update_module(db, module_request)


@router.get(
    "/search",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Search modules",
    description="Search for modules with pagination, search query, and status filters.",
)
async def search_modules(
    page: int = 0,
    size: int = 5,
    query: str = None,
    realm_id: int = None,
    application_id: int = None,
    active: bool = None,
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info(
        "module_router => search_modules function accessed: query=%s, realm_id=%s, application_id=%s, active=%s",
        query,
        realm_id,
        application_id,
        active,
    )
    return get_module_service().search_modules(
        db, page, size, query, realm_id, application_id, active
    )


@router.get(
    "/active",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Get all active modules",
    description="Retrieve list of all active modules.",
)
async def get_all_active_modules(db: Session = Depends(get_db)) -> CommonResponseDTO:
    logger.info("module_router => get_all_active_modules function accessed")
    return get_module_service().get_all_active_modules(db)


@router.get(
    "/get",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Get a module by ID",
    description="Retrieve a single module by its ID.",
)
async def get_module_by_id(
    module_id: int = Query(..., description="The ID of the module to retrieve"),
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info("module_router => get_module_by_id function accessed: %s", module_id)
    return get_module_service().get_module_by_id(db, module_id)


@router.delete(
    "/delete",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Delete a module by ID",
    description="Delete a single module by its ID.",
)
async def delete_module_by_id(
    module_id: int = Query(..., description="The ID of the module to delete"),
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info("module_router => delete_module_by_id function accessed: %s", module_id)
    return get_module_service().delete_module_by_id(db, module_id)
