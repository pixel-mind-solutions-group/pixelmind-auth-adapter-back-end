# Logs
import logging
import traceback

# Models
from models.realm.realm import Realm
from models.application.application import Application
from models.user_role.user_role import UserRole
from models.module.module import Module
from models.api_permission.api_permission import ApiPermission
from models.ui_permission.ui_permission import UiPermission
from models.user_role_has_modules_has_api_permission.user_role_has_modules_has_api_permission import (
    UserRoleHasModulesHasApiPermission,
)
from models.realms_has_applications.realms_has_applications import RealmsHasApplications

# Services
from services.user_role_profile.user_role_profile_service import (
    UserRoleProfileService,
)

# Schemas
from schemas.common_response import CommonResponseDTO
from schemas.user_role_profile.user_role_profile_request import (
    UserRoleProfileRequestDTO,
)
from schemas.user_role_profile.user_role_profile_sync_request import (
    UserRoleProfileSyncRequestDTO,
)
from schemas.user_role_profile.user_role_profile_search_response import (
    UserRoleProfileSearchResponseDTO,
)

from fastapi import status

# Exceptions
from exceptions.custom_exceptions import (
    AppException,
    BadRequestException,
    NotFoundException,
)

# Repositories
from repositories.user_role_profile.user_role_profile_repository import (
    UserRoleProfileRepository,
)
from repositories.realm.realm_repository import RealmRepository
from repositories.application.application_repository import ApplicationRepository
from repositories.user_role.user_role_repository import UserRoleRepository

# Mapper
import mapper.user_role_profile.user_role_profile_mapper as mapper

# Dependencies
from core.dependancies.clients.client_dependency import get_keycloak_client

# Client
from clients.keycloak.keycloak_client import KeycloakClient

logger = logging.getLogger(__name__)


class UserRoleProfileServiceImpl(UserRoleProfileService):

    def __init__(self):
        self.realmRepository: RealmRepository = RealmRepository()
        self.applicationRepository: ApplicationRepository = ApplicationRepository()
        self.userRoleRepository: UserRoleRepository = UserRoleRepository()
        self.repository = UserRoleProfileRepository()

    def create_profile(
        self, db: Session, req_data: UserRoleProfileRequestDTO
    ) -> CommonResponseDTO:
        logger.info("UserRoleProfileServiceImpl => create_profile: %s", req_data)

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

        # 3. Verify UserRole exists and belongs to the Realm/Application
        role = db.query(UserRole).filter(UserRole.id == req_data.userRoleId).first()
        if not role:
            raise NotFoundException(
                f"User Role with ID {req_data.userRoleId} not found"
            )
        if (
            role.realmId != req_data.realmId
            or role.applicationId != req_data.applicationId
        ):
            raise BadRequestException(
                f"User Role with ID {req_data.userRoleId} does not belong to the selected Realm/Application"
            )

        # 4. Validate Module IDs
        module_id_list = req_data.moduleIdList
        if not module_id_list:
            module_id_list = [None]

        for module_id in module_id_list:
            if module_id is not None:
                module = db.query(Module).filter(Module.id == module_id).first()
                if not module:
                    raise NotFoundException(f"Module with ID {module_id} not found")
                if (
                    module.realmId != req_data.realmId
                    or module.applicationId != req_data.applicationId
                ):
                    raise BadRequestException(
                        f"Module with name {module.moduleName} does not belong to the selected Realm/Application"
                    )

        # 5. Validate API Permission IDs
        for api_perm_id in req_data.apiPermissionIdList:
            api_perm = (
                db.query(ApiPermission).filter(ApiPermission.id == api_perm_id).first()
            )
            if not api_perm:
                raise NotFoundException(
                    f"API Permission with ID {api_perm_id} not found"
                )

        # 6. Validate UI Permission IDs
        for ui_perm_id in req_data.uiPermissionIdList:
            ui_perm = (
                db.query(UiPermission).filter(UiPermission.id == ui_perm_id).first()
            )
            if not ui_perm:
                raise NotFoundException(f"UI Permission with ID {ui_perm_id} not found")

        created_api_entities = []
        created_ui_entities = []

        # 7. Create API Mappings
        for module_id in module_id_list:
            for api_perm_id in req_data.apiPermissionIdList:
                existing = self.repository.find_api_by_composite(
                    db,
                    req_data.realmId,
                    req_data.applicationId,
                    req_data.userRoleId,
                    module_id,
                    api_perm_id,
                )
                if existing:
                    created_api_entities.append(existing)
                else:
                    entity = mapper.to_api_model(
                        req_data.realmId,
                        req_data.applicationId,
                        req_data.userRoleId,
                        module_id,
                        api_perm_id,
                    )
                    entity = self.repository.create_api(db, entity)
                    db.refresh(entity)
                    created_api_entities.append(entity)

        # 8. Create UI Mappings
        for module_id in module_id_list:
            for ui_perm_id in req_data.uiPermissionIdList:
                existing = self.repository.find_ui_by_composite(
                    db,
                    req_data.realmId,
                    req_data.applicationId,
                    req_data.userRoleId,
                    module_id,
                    ui_perm_id,
                )
                if existing:
                    created_ui_entities.append(existing)
                else:
                    entity = mapper.to_ui_model(
                        req_data.realmId,
                        req_data.applicationId,
                        req_data.userRoleId,
                        module_id,
                        ui_perm_id,
                    )
                    entity = self.repository.create_ui(db, entity)
                    db.refresh(entity)
                    created_ui_entities.append(entity)

        # 9. Map to search response DTO structure
        response_data = UserRoleProfileSearchResponseDTO(
            apiPermissions=mapper.to_api_dto_list(created_api_entities),
            uiPermissions=mapper.to_ui_dto_list(created_ui_entities),
        )

        return CommonResponseDTO(
            status=status.HTTP_201_CREATED,
            message="User Role Profile mappings updated successfully",
            data=response_data,
        )

    def delete_api_profile_by_id(
        self, db: Session, mapping_id: int
    ) -> CommonResponseDTO:
        logger.info(
            "UserRoleProfileServiceImpl => delete_api_profile_by_id: %s", mapping_id
        )
        mapping = self.repository.find_api_by_id(db, mapping_id)
        if not mapping:
            raise NotFoundException(
                f"User Role API Profile mapping with ID {mapping_id} not found"
            )

        self.repository.delete_api(db, mapping)

        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="User Role API Profile mapping deleted successfully",
            data=None,
        )

    def delete_ui_profile_by_id(
        self, db: Session, mapping_id: int
    ) -> CommonResponseDTO:
        logger.info(
            "UserRoleProfileServiceImpl => delete_ui_profile_by_id: %s", mapping_id
        )
        mapping = self.repository.find_ui_by_id(db, mapping_id)
        if not mapping:
            raise NotFoundException(
                f"User Role UI Profile mapping with ID {mapping_id} not found"
            )

        self.repository.delete_ui(db, mapping)

        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="User Role UI Profile mapping deleted successfully",
            data=None,
        )

    def search_assigned_profiles(
        self,
        db: Session,
        realm_id: int = None,
        application_id: int = None,
        user_role_id: int = None,
        module_id: int = None,
    ) -> CommonResponseDTO:
        logger.info(
            "UserRoleProfileServiceImpl => search_assigned_profiles: realm_id=%s, application_id=%s, user_role_id=%s, module_id=%s",
            realm_id,
            application_id,
            user_role_id,
            module_id,
        )
        api_mappings = self.repository.search_api_assigned(
            db, realm_id, application_id, user_role_id, module_id
        )
        ui_mappings = self.repository.search_ui_assigned(
            db, realm_id, application_id, user_role_id, module_id
        )

        response_data = UserRoleProfileSearchResponseDTO(
            apiPermissions=mapper.to_api_dto_list(api_mappings),
            uiPermissions=mapper.to_ui_dto_list(ui_mappings),
        )

        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="Assigned User Role profiles retrieved successfully",
            data=response_data,
        )

    def sync_profile(
        self, db: Session, req_data: UserRoleProfileSyncRequestDTO
    ) -> CommonResponseDTO:
        logger.info("UserRoleProfileServiceImpl => sync_profile: %s", req_data)

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

        # 3. Verify UserRole exists and belongs to the Realm/Application
        role = db.query(UserRole).filter(UserRole.id == req_data.userRoleId).first()
        if not role:
            raise NotFoundException(
                f"User Role with ID {req_data.userRoleId} not found"
            )
        if (
            role.realmId != req_data.realmId
            or role.applicationId != req_data.applicationId
        ):
            raise BadRequestException(
                f"User Role with ID {req_data.userRoleId} does not belong to the selected Realm/Application"
            )

        # 4. Validate all module and permission IDs before deleting
        for mod_sync in req_data.modules:
            if mod_sync.moduleId is not None:
                module = db.query(Module).filter(Module.id == mod_sync.moduleId).first()
                if not module:
                    raise NotFoundException(
                        f"Module with ID {mod_sync.moduleId} not found"
                    )
                if (
                    module.realmId != req_data.realmId
                    or module.applicationId != req_data.applicationId
                ):
                    raise BadRequestException(
                        f"Module with name {module.moduleName} does not belong to the selected Realm/Application"
                    )

            for api_perm_id in mod_sync.apiPermissionIdList:
                api_perm = (
                    db.query(ApiPermission)
                    .filter(ApiPermission.id == api_perm_id)
                    .first()
                )
                if not api_perm:
                    raise NotFoundException(
                        f"API Permission with ID {api_perm_id} not found"
                    )

            for ui_perm_id in mod_sync.uiPermissionIdList:
                ui_perm = (
                    db.query(UiPermission).filter(UiPermission.id == ui_perm_id).first()
                )
                if not ui_perm:
                    raise NotFoundException(
                        f"UI Permission with ID {ui_perm_id} not found"
                    )

        # 5. Clear all existing mappings for the role under this realm/app
        self.repository.delete_all_by_role(
            db, req_data.realmId, req_data.applicationId, req_data.userRoleId
        )

        # 6. Re-create mappings from sync payload
        created_api_entities = []
        created_ui_entities = []

        for mod_sync in req_data.modules:
            # Create API Mappings
            for api_perm_id in mod_sync.apiPermissionIdList:
                entity = mapper.to_api_model(
                    req_data.realmId,
                    req_data.applicationId,
                    req_data.userRoleId,
                    mod_sync.moduleId,
                    api_perm_id,
                )
                entity = self.repository.create_api(db, entity)
                db.refresh(entity)
                created_api_entities.append(entity)

            # Create UI Mappings
            for ui_perm_id in mod_sync.uiPermissionIdList:
                entity = mapper.to_ui_model(
                    req_data.realmId,
                    req_data.applicationId,
                    req_data.userRoleId,
                    mod_sync.moduleId,
                    ui_perm_id,
                )
                entity = self.repository.create_ui(db, entity)
                db.refresh(entity)
                created_ui_entities.append(entity)

        response_data = UserRoleProfileSearchResponseDTO(
            apiPermissions=mapper.to_api_dto_list(created_api_entities),
            uiPermissions=mapper.to_ui_dto_list(created_ui_entities),
        )

        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="User Role Profile mappings synchronized successfully",
            data=response_data,
        )

    def sync_user_role_api_permissions_of_realm_and_application(
        self, db: Session, realm_id: int, application_id: int, user_role_id: int
    ) -> CommonResponseDTO:
        logger.info(
            "UserRoleProfileServiceImpl => sync_user_role_api_permissions_of_realm_and_application: realm_id=%s, application_id=%s, user_role_id=%s",
            realm_id,
            application_id,
            user_role_id,
        )

        try:
            if realm_id is None:
                raise BadRequestException("Realm ID is required")

            if application_id is None:
                raise BadRequestException("Application ID is required")

            # realm and application repo
            realm = self.realmRepository.get_by_id(db, realm_id)
            if not realm:
                raise BadRequestException(f"Realm with ID {realm_id} not found")

            application = self.applicationRepository.get_by_id(db, application_id)
            if not application:
                raise NotFoundException(
                    f"Application with ID {application_id} not found"
                )

            if application.realm_id != realm_id:
                raise BadRequestException(
                    f"Application with ID {application_id} does not belong to Realm {realm_id}"
                )

            # Query user roles
            if user_role_id is not None:
                user_roles = self.userRoleRepository.get_user_role_of_realm_and_application_and_user_role_id(
                    db, realm_id, application_id, user_role_id
                )
                user_roles = [user_roles] if user_roles else []
            else:
                user_roles = (
                    self.userRoleRepository.get_all_user_roles_of_realm_and_application(
                        db, realm_id, application_id
                    )
                )

            if not user_roles:
                raise NotFoundException(
                    f"User Roles not found in Realm {realm_id} and Application {application_id}"
                )

            role_wise_api_permissions_list = []
            for user_role in user_roles:
                URHMAP = UserRoleHasModulesHasApiPermission
                AP = ApiPermission

                api_permissions = (
                    db.query(AP.apiPermissionName)
                    .join(URHMAP, URHMAP.apiPermissionId == AP.id)
                    .filter(
                        URHMAP.realmId == realm_id,
                        URHMAP.applicationId == application_id,
                        URHMAP.userRoleId == user_role.id,
                        AP.active == True,
                    )
                    .all()
                )

                api_permission_names = [name for (name,) in api_permissions]

                user_role_profile_permissions_sync_request_dto = {
                    "role_name": user_role.roleName,
                    "api_permissions_list": api_permission_names,
                }

                role_wise_api_permissions_list.append(
                    user_role_profile_permissions_sync_request_dto
                )

            logger.info(
                "role_wise_api_permissions_list=%s", role_wise_api_permissions_list
            )

            realm_app_mapping = (
                db.query(RealmsHasApplications)
                .filter(
                    RealmsHasApplications.realm_id == realm_id,
                    RealmsHasApplications.application_id == application_id,
                )
                .first()
            )
            if not realm_app_mapping:
                raise NotFoundException(
                    f"Realm has application mapping not found for realm ID {realm_id} and application ID {application_id}"
                )

            # calling keycloak service to sync
            keycloak_response = get_keycloak_client().sync_user_role_api_permissions_of_realm_and_application(
                realm_internal_uuid=realm.internal_uuid,
                application_internal_uuid=realm_app_mapping.internal_application_uuid,
                role_wise_permissions=role_wise_api_permissions_list,
            )

            return CommonResponseDTO(
                status=status.HTTP_200_OK,
                message="User Role Profile mappings synchronized successfully",
                data=role_wise_api_permissions_list,
            )

        except Exception as e:
            # Log full stack trace
            logger.error("Error syncing user role API permissions: %s", str(e))
            logger.error(traceback.format_exc())  # prints full stack trace

            return CommonResponseDTO(
                success=False, message="Internal Server Error", status=500
            )
