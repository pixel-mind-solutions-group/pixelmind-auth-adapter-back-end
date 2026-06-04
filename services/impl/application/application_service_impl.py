import logging

from fastapi import status
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO
from repositories.application.application_repository import ApplicationRepository
import mapper.application.application_mapper as application_mapper
from services.application.application_service import ApplicationService

logger = logging.getLogger(__name__)


class ApplicationServiceImpl(ApplicationService):

    def __init__(self):
        self.application_repository = ApplicationRepository()

    def get_all_applications(self, db: Session) -> CommonResponseDTO:
        logger.info("ApplicationServiceImpl => get_all_applications function accessed")

        applications = self.application_repository.get_all(db)
        application_dtos = application_mapper.to_dto_list(applications)

        logger.info("ApplicationServiceImpl => get_all_applications function ended")

        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="Applications retrieved successfully",
            data={"applications": application_dtos, "total": len(application_dtos)},
        )
