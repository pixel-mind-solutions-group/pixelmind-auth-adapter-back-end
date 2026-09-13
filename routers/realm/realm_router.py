import logging
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO
from core.dependancies.db.db import get_db
from core.dependancies.services.service_dependancy import get_realm_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/pixel-auth-adapter/realm", tags=["Realm"])


@router.post(
    "/sync",
    status_code=status.HTTP_200_OK,
    summary="Sync realms and applications from Keycloak",
    description="This endpoint fetches active realms and applications from Keycloak and syncs them to the DB.",
)
async def sync_realms_and_applications(
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info("realm_router => sync_realms_and_applications function accessed")
    return get_realm_service().sync_realms_and_applications(db)


@router.get(
    "/active",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Get all active realms",
    description="This endpoint retrieves all active realms from the database.",
)
async def get_all_active_realms(
    only_active: bool = True,
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info("realm_router => get_all_active_realms function accessed: only_active=%s", only_active)
    return get_realm_service().get_all_active_realms(db, only_active)


@router.delete(
    "/{realm_id}",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Delete realm and all related data",
    description="This endpoint deletes a realm and all associated data inside the database without validation.",
)
async def delete_realm(
    realm_id: int,
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info("realm_router => delete_realm function accessed: realm_id=%s", realm_id)
    return get_realm_service().delete_realm(db, realm_id)


@router.delete(
    "/{realm_id}/application/{application_id}",
    response_model=CommonResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Delete all data by realm and application",
    description="This endpoint deletes all data related to the specified realm and application inside the database without validation.",
)
async def delete_by_realm_and_application(
    realm_id: int,
    application_id: int,
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info(
        "realm_router => delete_by_realm_and_application function accessed: realm_id=%s, application_id=%s",
        realm_id,
        application_id,
    )
    return get_realm_service().delete_by_realm_and_application(
        db, realm_id, application_id
    )


