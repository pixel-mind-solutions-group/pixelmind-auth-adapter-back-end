import logging
from sqlalchemy.orm import Session
from fastapi import status
from exceptions.custom_exceptions import (
    BadRequestException,
    NotFoundException,
)
from schemas.common_response import CommonResponseDTO
from schemas.application_has_api_permission.application_has_api_permission_request import (
    ApplicationHasApiPermissionRequestDTO,
)
from models.realm.realm import Realm
from models.application.application import Application
from models.api_permission.api_permission import ApiPermission
from models.application_has_api_permission.application_has_api_permission import (
    ApplicationHasApiPermission,
)
from repositories.application_has_api_permission.application_has_api_permission_repository import (
    ApplicationHasApiPermissionRepository,
)
from services.application_has_api_permission.application_has_api_permission_service import (
    ApplicationHasApiPermissionService,
)
import mapper.application_has_api_permission.application_has_api_permission_mapper as mapper

logger = logging.getLogger(__name__)


class ApplicationHasApiPermissionServiceImpl(ApplicationHasApiPermissionService):

    def __init__(self):
        self.repository = ApplicationHasApiPermissionRepository()

    def create_profile(
        self, db: Session, req_data: ApplicationHasApiPermissionRequestDTO
    ) -> CommonResponseDTO:
        logger.info(
            "ApplicationHasApiPermissionServiceImpl => create_profile: %s", req_data
        )

        # 1. Verify Realm exists
        realm = db.query(Realm).filter(Realm.id == req_data.realmId).first()
        if not realm:
            raise NotFoundException(f"Realm with ID {req_data.realmId} not found")

        # 2. Verify Application exists
        app = (
            db.query(Application)
            .filter(Application.id == req_data.applicationId)
            .first()
        )
        if not app:
            raise NotFoundException(
                f"Application with ID {req_data.applicationId} not found"
            )

        # 3. Verify all API Permissions exist
        for perm_id in req_data.apiPermissionIdList:
            perm = db.query(ApiPermission).filter(ApiPermission.id == perm_id).first()
            if not perm:
                raise NotFoundException(f"API Permission with ID {perm_id} not found")

        # 4. Create and save new mappings without deleting previously saved records
        created_entities = []
        for perm_id in req_data.apiPermissionIdList:
            existing = self.repository.find_by_realm_app_and_permission(
                db, req_data.realmId, req_data.applicationId, perm_id
            )
            if existing:
                created_entities.append(existing)
            else:
                entity = mapper.to_model(
                    req_data.realmId, req_data.applicationId, perm_id
                )
                entity = self.repository.create(db, entity)
                # Ensure relationships are loaded
                db.refresh(entity)
                created_entities.append(entity)

        return CommonResponseDTO(
            status=status.HTTP_201_CREATED,
            message="Application API Permission mappings updated successfully",
            data=mapper.to_dto_list(created_entities),
        )

    def delete_profile_by_id(self, db: Session, mapping_id: int) -> CommonResponseDTO:
        logger.info(
            "ApplicationHasApiPermissionServiceImpl => delete_profile_by_id: %s",
            mapping_id,
        )

        mapping = self.repository.find_by_id(db, mapping_id)
        if not mapping:
            raise NotFoundException(
                f"Application API Permission mapping with ID {mapping_id} not found"
            )

        self.repository.delete(db, mapping)

        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="Application API Permission mapping deleted successfully",
            data=None,
        )

    def search_assigned_permissions(
        self,
        db: Session,
        realm_id: int = None,
        application_id: int = None,
        api_permission_name: str = None,
    ) -> CommonResponseDTO:
        logger.info(
            "ApplicationHasApiPermissionServiceImpl => search_assigned_permissions: realm_id=%s, application_id=%s, api_permission_name=%s",
            realm_id,
            application_id,
            api_permission_name,
        )
        mappings = self.repository.search_assigned(
            db, realm_id, application_id, api_permission_name
        )
        dtos = mapper.to_dto_list(mappings)
        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="Assigned API permissions retrieved successfully",
            data=dtos,
        )
