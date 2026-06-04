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

    def search_applications(
        self, db: Session, page: int, size: int, query: str
    ) -> CommonResponseDTO:
        logger.info(
            "ApplicationServiceImpl => search_applications function accessed: %s", query
        )

        applications, total_pages, total = self.application_repository.search(
            db, page, size, query
        )
        application_dtos = application_mapper.to_dto_list(applications)

        logger.info(
            "ApplicationServiceImpl => search_applications function ended: %s", query
        )

        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="Applications retrieved successfully",
            data={
                "applications": application_dtos,
                "total": total,
                "page": page,
                "size": size,
                "totalPages": total_pages,
            },
        )
