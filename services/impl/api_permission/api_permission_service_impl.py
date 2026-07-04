import logging
from datetime import datetime
from sqlalchemy import null
from sqlalchemy.orm import Session
from fastapi import status
from exceptions.custom_exceptions import (
    AppException,
    BadRequestException,
    NotFoundException,
)
from schemas.common_response import CommonResponseDTO
from schemas.api_permission.api_permission_request import ApiPermissionRequestDTO
from repositories.api_permission.api_permission_repository import (
    ApiPermissionRepository,
)
import mapper.api_permission.api_permission_mapper as api_permission_mapper
from models.api_permission.api_permission import ApiPermission
from models.realm.realm import Realm
from models.application_has_api_permission.application_has_api_permission import ApplicationHasApiPermission
from core.dependancies.clients.client_dependency import get_keycloak_client
from services.api_permission.api_permission_service import ApiPermissionService

logger = logging.getLogger(__name__)


class ApiPermissionServiceImpl(ApiPermissionService):

    def __init__(self, keycloak_client=None):
        self.repository = ApiPermissionRepository()
        self.keycloak_client = keycloak_client or get_keycloak_client()

    def create_or_update_permission(
        self, db: Session, req_data: ApiPermissionRequestDTO
    ) -> CommonResponseDTO:
        logger.info(
            "ApiPermissionServiceImpl => create_or_update_permission: %s", req_data
        )

        # Check unique constraint globally
        existing = self.repository.find_by_name(db, req_data.apiPermissionName)
        if existing and (
            not req_data.apiPermissionId or existing.id != req_data.apiPermissionId
        ):
            raise BadRequestException(
                f"Permission name '{req_data.apiPermissionName}' already exists"
            )

        message = None
        entity: ApiPermission = None
        is_update = False
        old_name = None

        if req_data.apiPermissionId and req_data.apiPermissionId != null:
            entity = self.repository.find_by_id(db, req_data.apiPermissionId)
            if not entity:
                raise NotFoundException(
                    f"Permission with ID {req_data.apiPermissionId} not found"
                )
            is_update = True
            old_name = entity.apiPermissionName
            entity.updatedAt = datetime.now()
            entity.updatedBy = "system"
            message = "Permission updated successfully"
        else:
            entity = ApiPermission()
            entity.createdAt = datetime.now()
            entity.createdBy = "system"
            message = "Permission created successfully"

        entity = api_permission_mapper.to_model(entity, req_data)

        # Propagate role management to Keycloak active realms
        active_realms = db.query(Realm).filter(Realm.active == True).all()
        for r in active_realms:
            if is_update:
                self.keycloak_client.update_realm_role(
                    realm_name=r.realm,
                    old_role_name=old_name,
                    new_role_name=entity.apiPermissionName,
                    description=entity.description
                )
            else:
                self.keycloak_client.create_realm_role(
                    realm_name=r.realm,
                    role_name=entity.apiPermissionName,
                    description=entity.description
                )

        try:
            entity = self.repository.create(db, entity)
        except Exception as e:
            logger.error("Error creating/updating permission: %s", e)
            raise AppException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Failed to create or update permission",
            )

        return CommonResponseDTO(
            status=status.HTTP_201_CREATED,
            message=message,
            data=api_permission_mapper.to_dto(entity),
        )

    def get_permission_by_id(self, db: Session, perm_id: int) -> CommonResponseDTO:
        logger.info("ApiPermissionServiceImpl => get_permission_by_id: %s", perm_id)
        entity = self.repository.find_by_id(db, perm_id)
        if not entity:
            raise NotFoundException(f"Permission with ID {perm_id} not found")

        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="Permission retrieved successfully",
            data=api_permission_mapper.to_dto(entity),
        )

    def delete_permission_by_id(self, db: Session, perm_id: int) -> CommonResponseDTO:
        logger.info("ApiPermissionServiceImpl => delete_permission_by_id: %s", perm_id)
        entity = self.repository.find_by_id(db, perm_id)
        if not entity:
            raise NotFoundException(f"Permission with ID {perm_id} not found")

        # Validation: check if api permission is assigned to any application (profile mapping)
        assigned = (
            db.query(ApplicationHasApiPermission)
            .filter(ApplicationHasApiPermission.apiPermissionId == perm_id)
            .first()
        )
        if assigned:
            raise BadRequestException(
                f"Cannot delete permission '{entity.apiPermissionName}' as it is currently mapped to one or more applications"
            )

        # Delete module mappings referencing this API permission
        from models.module_has_api_permission.module_has_api_permission import ModuleHasApiPermission
        module_mappings = (
            db.query(ModuleHasApiPermission)
            .filter(ModuleHasApiPermission.apiPermissionId == perm_id)
            .all()
        )
        for m_map in module_mappings:
            db.delete(m_map)

        # Delete user role profiles referencing this API permission
        from models.user_role_has_modules_has_api_permission.user_role_has_modules_has_api_permission import UserRoleHasModulesHasApiPermission
        user_role_mappings = (
            db.query(UserRoleHasModulesHasApiPermission)
            .filter(UserRoleHasModulesHasApiPermission.apiPermissionId == perm_id)
            .all()
        )
        for ur_map in user_role_mappings:
            db.delete(ur_map)

        # Propagate realm role deletion to Keycloak active realms
        active_realms = db.query(Realm).filter(Realm.active == True).all()
        for r in active_realms:
            try:
                self.keycloak_client.delete_realm_role(
                    realm_name=r.realm,
                    role_name=entity.apiPermissionName
                )
            except Exception as e:
                logger.error("Failed to delete realm role %s in Keycloak: %s", entity.apiPermissionName, e)

        # Delete the permission definition
        self.repository.delete(db, entity)

        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="Permission deleted successfully",
            data=None,
        )

    def search_permissions(
        self,
        db: Session,
        page: int,
        size: int,
        query: str,
        active: bool = None,
    ) -> CommonResponseDTO:
        logger.info(
            "ApiPermissionServiceImpl => search_permissions: query=%s, active=%s",
            query,
            active,
        )
        perms, total_pages, total = self.repository.search(
            db, page, size, query, active
        )
        dtos = api_permission_mapper.to_dto_list(perms)

        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="Permissions retrieved successfully",
            data={
                "permissions": dtos,
                "total": total,
                "page": page,
                "size": size,
                "totalPages": total_pages,
            },
        )

    def get_all_active_permissions(
        self,
        db: Session,
        realm_id: int,
        application_id: int,
        api_permission_name: str = None,
    ) -> CommonResponseDTO:
        logger.info(
            "ApiPermissionServiceImpl => get_all_active_permissions: realm_id=%s, application_id=%s, api_permission_name=%s",
            realm_id,
            application_id,
            api_permission_name,
        )
        perms = self.repository.get_all_active_permissions(
            db, realm_id, application_id, api_permission_name
        )
        dtos = api_permission_mapper.to_dto_list(perms)

        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="Active permissions retrieved successfully",
            data=dtos,
        )
