import logging
from fastapi import status
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO
from repositories.realm.realm_repository import RealmRepository
import mapper.realm.realm_mapper as realm_mapper
from services.realm.realm_service import RealmService

logger = logging.getLogger(__name__)


class RealmServiceImpl(RealmService):

    def __init__(self):
        self.realm_repository = RealmRepository()

    def get_all_active_realms(self, db: Session) -> CommonResponseDTO:
        logger.info("RealmServiceImpl => get_all_active_realms function accessed")
        realms = self.realm_repository.get_all_active_realms(db)
        realm_dtos = realm_mapper.to_dto_list(realms)

        logger.info("RealmServiceImpl => get_all_active_realms function ended")
        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="Active realms retrieved successfully",
            data=realm_dtos,
        )
