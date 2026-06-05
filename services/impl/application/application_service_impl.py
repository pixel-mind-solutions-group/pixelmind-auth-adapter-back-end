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

    def get_all_active_applications(self, db: Session) -> CommonResponseDTO:
        logger.info(
            "ApplicationServiceImpl => get_all_active_applications function accessed"
        )
        applications = self.application_repository.get_all_active_applications(db)
        application_dtos = application_mapper.to_dto_list(applications)

        logger.info(
            "ApplicationServiceImpl => get_all_active_applications function ended"
        )
        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="Active applications retrieved successfully",
            data=application_dtos,
        )

    def search_applications(
        self,
        db: Session,
        page: int,
        size: int,
        query: str = None,
        realm_id: int = None,
        application_id: int = None,
    ) -> CommonResponseDTO:
        logger.info(
            "ApplicationServiceImpl => search_applications function accessed: query=%s, realm_id=%s, application_id=%s",
            query,
            realm_id,
            application_id,
        )

        applications, total_pages, total = self.application_repository.search(
            db, page, size, query, realm_id, application_id
        )
        application_dtos = application_mapper.to_dto_list(applications)

        logger.info("ApplicationServiceImpl => search_applications function ended")

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
