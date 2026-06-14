import logging
from sqlalchemy.orm import Session
from fastapi import status
from exceptions.custom_exceptions import (
    BadRequestException,
    NotFoundException,
)
from schemas.common_response import CommonResponseDTO
from schemas.module_has_api_permission.module_has_api_permission_request import (
    ModuleHasApiPermissionRequestDTO,
)
from models.module.module import Module
from models.api_permission.api_permission import ApiPermission
from models.module_has_api_permission.module_has_api_permission import (
    ModuleHasApiPermission,
)
from models.application_has_api_permission.application_has_api_permission import (
    ApplicationHasApiPermission,
)
from repositories.module_has_api_permission.module_has_api_permission_repository import (
    ModuleHasApiPermissionRepository,
)
from services.module_has_api_permission.module_has_api_permission_service import (
    ModuleHasApiPermissionService,
)
import mapper.module_has_api_permission.module_has_api_permission_mapper as mapper

logger = logging.getLogger(__name__)


class ModuleHasApiPermissionServiceImpl(ModuleHasApiPermissionService):

    def __init__(self):
        self.repository = ModuleHasApiPermissionRepository()

    def create_profile(
        self, db: Session, req_data: ModuleHasApiPermissionRequestDTO
    ) -> CommonResponseDTO:
        logger.info("ModuleHasApiPermissionServiceImpl => create_profile: %s", req_data)

        # 1. Verify Module exists
        module = db.query(Module).filter(Module.id == req_data.moduleId).first()
        if not module:
            raise NotFoundException(f"Module with ID {req_data.moduleId} not found")

        # Validate that the list is not empty and does not contain null values
        if not req_data.apiPermissionIdList:
            raise BadRequestException("API Permission list cannot be empty")
        if any(p is None for p in req_data.apiPermissionIdList):
            raise BadRequestException("API Permission ID cannot be null")

        # 2. Verify all API Permissions exist
        for perm_id in req_data.apiPermissionIdList:
            perm = db.query(ApiPermission).filter(ApiPermission.id == perm_id).first()
            if not perm:
                raise NotFoundException(f"API Permission with ID {perm_id} not found")
            else:
                # Verify that the API permission is assigned to the Application containing this Module
                app_has_perm = (
                    db.query(ApplicationHasApiPermission)
                    .filter(
                        ApplicationHasApiPermission.realmId == module.realmId,
                        ApplicationHasApiPermission.applicationId == module.applicationId,
                        ApplicationHasApiPermission.apiPermissionId == perm_id,
                    )
                    .first()
                )
                if not app_has_perm:
                    raise BadRequestException(
                        f"API Permission with ID {perm_id} is not assigned to the Application of this Module"
                    )

        # 3. Create and save new mappings without deleting previously saved records
        created_entities = []
        for perm_id in req_data.apiPermissionIdList:
            existing = self.repository.find_by_module_and_permission(
                db, req_data.moduleId, perm_id
            )
            if existing:
                created_entities.append(existing)
            else:
                entity = mapper.to_model(req_data.moduleId, perm_id)
                entity = self.repository.create(db, entity)
                # Ensure relationships are loaded
                db.refresh(entity)
                created_entities.append(entity)

        return CommonResponseDTO(
            status=status.HTTP_201_CREATED,
            message="Module API Permission mappings updated successfully",
            data=mapper.to_dto_list(created_entities),
        )

    def delete_profile_by_id(self, db: Session, mapping_id: int) -> CommonResponseDTO:
        logger.info(
            "ModuleHasApiPermissionServiceImpl => delete_profile_by_id: %s",
            mapping_id,
        )

        mapping = self.repository.find_by_id(db, mapping_id)
        if not mapping:
            raise NotFoundException(
                f"Module API Permission mapping with ID {mapping_id} not found"
            )

        self.repository.delete(db, mapping)

        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="Module API Permission mapping deleted successfully",
            data=None,
        )

    def search_assigned_permissions(
        self,
        db: Session,
        realm_id: int = None,
        application_id: int = None,
        module_id: int = None,
        api_permission_name: str = None,
    ) -> CommonResponseDTO:
        logger.info(
            "ModuleHasApiPermissionServiceImpl => search_assigned_permissions: realm_id=%s, application_id=%s, module_id=%s, api_permission_name=%s",
            realm_id,
            application_id,
            module_id,
            api_permission_name,
        )
        mappings = self.repository.search_assigned(
            db, realm_id, application_id, module_id, api_permission_name
        )
        dtos = mapper.to_dto_list(mappings)
        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="Assigned Module API permissions retrieved successfully",
            data=dtos,
        )
