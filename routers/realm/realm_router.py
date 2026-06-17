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
    db: Session = Depends(get_db),
) -> CommonResponseDTO:
    logger.info("realm_router => get_all_active_realms function accessed")
    return get_realm_service().get_all_active_realms(db)
