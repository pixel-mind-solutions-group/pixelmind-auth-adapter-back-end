import logging
from sqlalchemy.orm import Session
from fastapi import status
from exceptions.custom_exceptions import (
    BadRequestException,
    NotFoundException,
)
from schemas.common_response import CommonResponseDTO
from schemas.user_role_has_modules.user_role_has_modules_request import (
    UserRoleHasModulesRequestDTO,
)
from models.realm.realm import Realm
from models.application.application import Application
from models.user_role.user_role import UserRole
from models.module.module import Module
from models.user_role_has_modules.user_role_has_modules import UserRoleHasModules
from repositories.user_role_has_modules.user_role_has_modules_repository import (
    UserRoleHasModulesRepository,
)
from services.user_role_has_modules.user_role_has_modules_service import (
    UserRoleHasModulesService,
)
import mapper.user_role_has_modules.user_role_has_modules_mapper as user_role_has_modules_mapper

logger = logging.getLogger(__name__)


class UserRoleHasModulesServiceImpl(UserRoleHasModulesService):

    def __init__(self):
        self.repository = UserRoleHasModulesRepository()

    def create_profile(
        self, db: Session, req_data: UserRoleHasModulesRequestDTO
    ) -> CommonResponseDTO:
        logger.info("UserRoleHasModulesServiceImpl => create_profile: %s", req_data)

        # 1. Verify Realm exists
        realm = db.query(Realm).filter(Realm.id == req_data.realmId).first()
        if not realm:
            raise NotFoundException(f"Realm with ID {req_data.realmId} not found")

        # 2. Verify Application exists
        app = db.query(Application).filter(Application.id == req_data.applicationId).first()
        if not app:
            raise NotFoundException(f"Application with ID {req_data.applicationId} not found")

        # 3. Verify UserRole exists
        role = db.query(UserRole).filter(UserRole.id == req_data.userRoleId).first()
        if not role:
            raise NotFoundException(f"User Role with ID {req_data.userRoleId} not found")

        # 4. Validate Module IDs
        if not req_data.moduleIdList:
            # If moduleIdList is empty, default it to [None] to assign to application level
            req_data.moduleIdList = [None]

        for module_id in req_data.moduleIdList:
            if module_id is not None:
                module = db.query(Module).filter(Module.id == module_id).first()
                if not module:
                    raise NotFoundException(f"Module with ID {module_id} not found")
                # Verify module belongs to application & realm
                if module.realmId != req_data.realmId or module.applicationId != req_data.applicationId:
                    raise BadRequestException(
                        f"Module with name {module.moduleName} does not belong to the selected Realm/Application"
                    )

        # 5. Create and save new mappings without deleting previously saved records
        created_entities = []
        for module_id in req_data.moduleIdList:
            existing = self.repository.find_by_realm_app_role_and_module(
                db, req_data.realmId, req_data.applicationId, req_data.userRoleId, module_id
            )
            if existing:
                created_entities.append(existing)
            else:
                entity = user_role_has_modules_mapper.to_model(
                    req_data.realmId, req_data.applicationId, req_data.userRoleId, module_id
                )
                entity = self.repository.create(db, entity)
                db.refresh(entity)
                created_entities.append(entity)

        return CommonResponseDTO(
            status=status.HTTP_201_CREATED,
            message="User Role Profile mappings updated successfully",
            data=user_role_has_modules_mapper.to_dto_list(created_entities),
        )

    def delete_profile_by_id(self, db: Session, mapping_id: int) -> CommonResponseDTO:
        logger.info("UserRoleHasModulesServiceImpl => delete_profile_by_id: %s", mapping_id)
        mapping = self.repository.find_by_id(db, mapping_id)
        if not mapping:
            raise NotFoundException(f"User Role Profile mapping with ID {mapping_id} not found")

        self.repository.delete(db, mapping)

        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="User Role Profile mapping deleted successfully",
            data=None,
        )

    def search_assigned_profiles(
        self,
        db: Session,
        realm_id: int = None,
        application_id: int = None,
    ) -> CommonResponseDTO:
        logger.info(
            "UserRoleHasModulesServiceImpl => search_assigned_profiles: realm_id=%s, application_id=%s",
            realm_id,
            application_id,
        )
        mappings = self.repository.search_assigned(db, realm_id, application_id)
        dtos = user_role_has_modules_mapper.to_dto_list(mappings)
        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="Assigned User Role profiles retrieved successfully",
            data=dtos,
        )
