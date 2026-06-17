import logging
from fastapi import status
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO
from repositories.application.application_repository import ApplicationRepository
import mapper.application.application_mapper as application_mapper
from services.application.application_service import ApplicationService
from models.application.application import Application
from models.realms_has_applications.realms_has_applications import RealmsHasApplications
from models.realm.realm import Realm

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

    def save_client_list_while_sync(
        self, db: Session, realm: Realm, clients_data: list
    ) -> None:
        logger.info(
            f"ApplicationServiceImpl => save_client_list_while_sync accessed for realm {realm.realm}"
        )

        active_internal_uuids = set()

        for client_data in clients_data:
            internal_uuid = client_data.get("id")
            client_id = client_data.get("clientId")
            is_active = client_data.get("active", True) if realm.active else False

            if not internal_uuid or not client_id:
                continue

            active_internal_uuids.add(internal_uuid)

            # 1. Lookup mapping by keycloak client ID (internal_application_uuid)
            mapping = (
                db.query(RealmsHasApplications)
                .filter(
                    RealmsHasApplications.internal_application_uuid == internal_uuid
                )
                .first()
            )

            if mapping:
                # Get existing application
                app_obj = (
                    db.query(Application)
                    .filter(Application.id == mapping.application_id)
                    .first()
                )
                if app_obj:
                    app_obj.clientId = client_id
                    app_obj.active = is_active
                mapping.realm_id = realm.id
            else:
                # Check if Application exists with the same client_id
                app_obj = (
                    db.query(Application)
                    .filter(Application.clientId == client_id)
                    .first()
                )
                if not app_obj:
                    app_obj = Application(clientId=client_id, active=is_active)
                    db.add(app_obj)
                    db.flush()
                else:
                    app_obj.active = is_active

                # Create a new mapping
                mapping = RealmsHasApplications(
                    internal_application_uuid=internal_uuid,
                    application_id=app_obj.id,
                    realm_id=realm.id,
                )
                db.add(mapping)

        db.flush()

    def deactivate_inactive_applications(
        self, db: Session, active_internal_uuids: list
    ) -> None:
        logger.info(
            "ApplicationServiceImpl => deactivate_inactive_applications accessed"
        )
        inactive_apps_query = db.query(RealmsHasApplications.application_id)
        if active_internal_uuids:
            inactive_apps_query = inactive_apps_query.filter(
                RealmsHasApplications.internal_application_uuid.not_in(
                    active_internal_uuids
                )
            )

        db.query(Application).filter(Application.id.in_(inactive_apps_query)).update(
            {Application.active: False}, synchronize_session=False
        )
        db.flush()
