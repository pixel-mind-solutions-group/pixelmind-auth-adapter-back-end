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
from schemas.ui_permission.ui_permission_request import UiPermissionRequestDTO
from repositories.ui_permission.ui_permission_repository import (
    UiPermissionRepository,
)
import mapper.ui_permission.ui_permission_mapper as ui_permission_mapper
from models.ui_permission.ui_permission import UiPermission
from services.ui_permission.ui_permission_service import UiPermissionService

logger = logging.getLogger(__name__)


class UiPermissionServiceImpl(UiPermissionService):

    def __init__(self):
        self.repository = UiPermissionRepository()

    def create_or_update_permission(
        self, db: Session, req_data: UiPermissionRequestDTO
    ) -> CommonResponseDTO:
        logger.info(
            "UiPermissionServiceImpl => create_or_update_permission: %s", req_data
        )

        # Check unique constraint globally
        existing = self.repository.find_by_name(db, req_data.uiPermissionName)
        if existing and (
            not req_data.uiPermissionId or existing.id != req_data.uiPermissionId
        ):
            raise BadRequestException(
                f"Permission name '{req_data.uiPermissionName}' already exists"
            )

        message = None
        entity: UiPermission = None

        if req_data.uiPermissionId and req_data.uiPermissionId != null:
            entity = self.repository.find_by_id(db, req_data.uiPermissionId)
            if not entity:
                raise NotFoundException(
                    f"Permission with ID {req_data.uiPermissionId} not found"
                )
            entity.updatedAt = datetime.now()
            entity.updatedBy = "system"
            message = "Permission updated successfully"
        else:
            entity = UiPermission()
            entity.createdAt = datetime.now()
            entity.createdBy = "system"
            message = "Permission created successfully"

        entity = ui_permission_mapper.to_model(entity, req_data)

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
            data=ui_permission_mapper.to_dto(entity),
        )

    def get_permission_by_id(self, db: Session, perm_id: int) -> CommonResponseDTO:
        logger.info("UiPermissionServiceImpl => get_permission_by_id: %s", perm_id)
        entity = self.repository.find_by_id(db, perm_id)
        if not entity:
            raise NotFoundException(f"Permission with ID {perm_id} not found")

        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="Permission retrieved successfully",
            data=ui_permission_mapper.to_dto(entity),
        )

    def delete_permission_by_id(self, db: Session, perm_id: int) -> CommonResponseDTO:
        logger.info("UiPermissionServiceImpl => delete_permission_by_id: %s", perm_id)
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
            "UiPermissionServiceImpl => search_permissions: query=%s, active=%s",
            query,
            active,
        )
        perms, total_pages, total = self.repository.search(
            db, page, size, query, active
        )
        dtos = ui_permission_mapper.to_dto_list(perms)

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
        ui_permission_name: str = None,
    ) -> CommonResponseDTO:
        logger.info(
            "UiPermissionServiceImpl => get_all_active_permissions: realm_id=%s, application_id=%s, ui_permission_name=%s",
            realm_id,
            application_id,
            ui_permission_name,
        )
        perms = self.repository.get_all_active_permissions(
            db, realm_id, application_id, ui_permission_name
        )
        dtos = ui_permission_mapper.to_dto_list(perms)

        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="Active permissions retrieved successfully",
            data=dtos,
        )
