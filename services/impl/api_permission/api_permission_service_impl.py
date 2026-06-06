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
from services.api_permission.api_permission_service import ApiPermissionService

logger = logging.getLogger(__name__)


class ApiPermissionServiceImpl(ApiPermissionService):

    def __init__(self):
        self.repository = ApiPermissionRepository()

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

        if req_data.apiPermissionId and req_data.apiPermissionId != null:
            entity = self.repository.find_by_id(db, req_data.apiPermissionId)
            if not entity:
                raise NotFoundException(
                    f"Permission with ID {req_data.apiPermissionId} not found"
                )
            entity.updatedAt = datetime.now()
            entity.updatedBy = "system"
            message = "Permission updated successfully"
        else:
            entity = ApiPermission()
            entity.createdAt = datetime.now()
            entity.createdBy = "system"
            message = "Permission created successfully"

        entity = api_permission_mapper.to_model(entity, req_data)

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
