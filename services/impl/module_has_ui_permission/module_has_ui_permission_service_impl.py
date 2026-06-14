import logging
from sqlalchemy.orm import Session
from fastapi import status
from exceptions.custom_exceptions import (
    BadRequestException,
    NotFoundException,
)
from schemas.common_response import CommonResponseDTO
from schemas.module_has_ui_permission.module_has_ui_permission_request import (
    ModuleHasUiPermissionRequestDTO,
)
from models.module.module import Module
from models.ui_permission.ui_permission import UiPermission
from models.module_has_ui_permission.module_has_ui_permission import (
    ModuleHasUiPermission,
)
from models.application_has_ui_permission.application_has_ui_permission import (
    ApplicationHasUiPermission,
)
from repositories.module_has_ui_permission.module_has_ui_permission_repository import (
    ModuleHasUiPermissionRepository,
)
from services.module_has_ui_permission.module_has_ui_permission_service import (
    ModuleHasUiPermissionService,
)
import mapper.module_has_ui_permission.module_has_ui_permission_mapper as mapper

logger = logging.getLogger(__name__)


class ModuleHasUiPermissionServiceImpl(ModuleHasUiPermissionService):

    def __init__(self):
        self.repository = ModuleHasUiPermissionRepository()

    def create_profile(
        self, db: Session, req_data: ModuleHasUiPermissionRequestDTO
    ) -> CommonResponseDTO:
        logger.info("ModuleHasUiPermissionServiceImpl => create_profile: %s", req_data)

        # 1. Verify Module exists
        module = db.query(Module).filter(Module.id == req_data.moduleId).first()
        if not module:
            raise NotFoundException(f"Module with ID {req_data.moduleId} not found")

        # Validate that the list is not empty and does not contain null values
        if not req_data.uiPermissionIdList:
            raise BadRequestException("UI Permission list cannot be empty")
        if any(p is None for p in req_data.uiPermissionIdList):
            raise BadRequestException("UI Permission ID cannot be null")

        # 2. Verify all UI Permissions exist
        for perm_id in req_data.uiPermissionIdList:
            perm = db.query(UiPermission).filter(UiPermission.id == perm_id).first()
            if not perm:
                raise NotFoundException(f"UI Permission with ID {perm_id} not found")
            else:
                # Verify that the UI permission is assigned to the Application containing this Module
                app_has_perm = (
                    db.query(ApplicationHasUiPermission)
                    .filter(
                        ApplicationHasUiPermission.realmId == module.realmId,
                        ApplicationHasUiPermission.applicationId == module.applicationId,
                        ApplicationHasUiPermission.uiPermissionId == perm_id,
                    )
                    .first()
                )
                if not app_has_perm:
                    raise BadRequestException(
                        f"UI Permission with UI Permission name {perm.uiPermissionName} is not assigned to the Application of this Module"
                    )

        # 3. Create and save new mappings without deleting previously saved records
        created_entities = []
        for perm_id in req_data.uiPermissionIdList:
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
            message="Module UI Permission mappings updated successfully",
            data=mapper.to_dto_list(created_entities),
        )

    def delete_profile_by_id(self, db: Session, mapping_id: int) -> CommonResponseDTO:
        logger.info(
            "ModuleHasUiPermissionServiceImpl => delete_profile_by_id: %s",
            mapping_id,
        )

        mapping = self.repository.find_by_id(db, mapping_id)
        if not mapping:
            raise NotFoundException(
                f"Module UI Permission mapping with ID {mapping_id} not found"
            )

        self.repository.delete(db, mapping)

        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="Module UI Permission mapping deleted successfully",
            data=None,
        )

    def search_assigned_permissions(
        self,
        db: Session,
        realm_id: int = None,
        application_id: int = None,
        module_id: int = None,
        query: str = None,
    ) -> CommonResponseDTO:
        logger.info(
            "ModuleHasUiPermissionServiceImpl => search_assigned_permissions: realm_id=%s, application_id=%s, module_id=%s, query=%s",
            realm_id,
            application_id,
            module_id,
            query,
        )
        mappings = self.repository.search_assigned(
            db, realm_id, application_id, module_id, query
        )
        dtos = mapper.to_dto_list(mappings)
        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="Assigned Module UI permissions retrieved successfully",
            data=dtos,
        )
