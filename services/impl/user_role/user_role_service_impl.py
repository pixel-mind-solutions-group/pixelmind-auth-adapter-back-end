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
from schemas.user_role.user_role_request import UserRoleRequestDTO
from repositories.user_role.user_role_repository import UserRoleRepository
import mapper.user_role.user_role_mapper as user_role_mapper
from models.user_role.user_role import UserRole
from models.realm.realm import Realm
from models.application.application import Application
from services.user_role.user_role_service import UserRoleService

logger = logging.getLogger(__name__)


class UserRoleServiceImpl(UserRoleService):

    def __init__(self):
        self.repository = UserRoleRepository()

    def create_or_update_role(
        self, db: Session, req_data: UserRoleRequestDTO
    ) -> CommonResponseDTO:
        logger.info("UserRoleServiceImpl => create_or_update_role: %s", req_data)

        # 1. Verify Realm exists
        realm = db.query(Realm).filter(Realm.id == req_data.realmId).first()
        if not realm:
            raise NotFoundException(f"Realm with ID {req_data.realmId} not found")

        # 2. Verify Application exists
        app = db.query(Application).filter(Application.id == req_data.applicationId).first()
        if not app:
            raise NotFoundException(f"Application with ID {req_data.applicationId} not found")

        # 3. Check unique constraint (scoped to Realm and Application)
        existing = self.repository.find_by_name_realm_app(
            db, req_data.roleName, req_data.realmId, req_data.applicationId
        )
        if existing and (
            not req_data.roleId or existing.id != req_data.roleId
        ):
            raise BadRequestException(
                f"Role name '{req_data.roleName}' already exists under this Realm and Application"
            )

        message = None
        entity: UserRole = None

        if req_data.roleId and req_data.roleId != null:
            entity = self.repository.find_by_id(db, req_data.roleId)
            if not entity:
                raise NotFoundException(
                    f"Role with ID {req_data.roleId} not found"
                )
            entity.updatedAt = datetime.now()
            entity.updatedBy = "system"
            message = "Role updated successfully"
        else:
            entity = UserRole()
            entity.createdAt = datetime.now()
            entity.createdBy = "system"
            message = "Role created successfully"

        entity = user_role_mapper.to_model(entity, req_data)

        try:
            entity = self.repository.create(db, entity)
            # Ensure relationships are loaded for response mapping
            db.refresh(entity)
        except Exception as e:
            logger.error("Error creating/updating role: %s", e)
            raise AppException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Failed to create or update role",
            )

        return CommonResponseDTO(
            status=status.HTTP_201_CREATED,
            message=message,
            data=user_role_mapper.to_dto(entity),
        )

    def get_role_by_id(self, db: Session, role_id: int) -> CommonResponseDTO:
        logger.info("UserRoleServiceImpl => get_role_by_id: %s", role_id)
        entity = self.repository.find_by_id(db, role_id)
        if not entity:
            raise NotFoundException(f"Role with ID {role_id} not found")

        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="Role retrieved successfully",
            data=user_role_mapper.to_dto(entity),
        )

    def delete_role_by_id(self, db: Session, role_id: int) -> CommonResponseDTO:
        logger.info("UserRoleServiceImpl => delete_role_by_id: %s", role_id)
        entity = self.repository.find_by_id(db, role_id)
        if not entity:
            raise NotFoundException(f"Role with ID {role_id} not found")

        try:
            self.repository.delete(db, entity)
        except Exception as e:
            logger.error("Error deleting role: %s", e)
            raise BadRequestException(
                "Cannot delete role as it is currently assigned or in use."
            )

        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="Role deleted successfully",
            data=None,
        )

    def search_roles(
        self,
        db: Session,
        page: int,
        size: int,
        query: str = None,
        active: bool = None,
        realm_id: int = None,
        application_id: int = None,
    ) -> CommonResponseDTO:
        logger.info(
            "UserRoleServiceImpl => search_roles: page=%s, size=%s, query=%s, active=%s, realm_id=%s, application_id=%s",
            page,
            size,
            query,
            active,
            realm_id,
            application_id,
        )
        roles, total_pages, total = self.repository.search(
            db, page, size, query, active, realm_id, application_id
        )
        dtos = user_role_mapper.to_dto_list(roles)

        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="Roles retrieved successfully",
            data={
                "roles": dtos,
                "total": total,
                "page": page,
                "size": size,
                "totalPages": total_pages,
            },
        )

    def get_all_active_roles(
        self,
        db: Session,
        realm_id: int = None,
        application_id: int = None,
    ) -> CommonResponseDTO:
        logger.info(
            "UserRoleServiceImpl => get_all_active_roles: realm_id=%s, application_id=%s",
            realm_id,
            application_id,
        )
        roles = self.repository.get_all_active(db, realm_id, application_id)
        dtos = user_role_mapper.to_dto_list(roles)
        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="Active roles retrieved successfully",
            data=dtos,
        )
