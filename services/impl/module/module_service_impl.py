import logging
from sqlalchemy import null
from sqlalchemy.orm import Session
from fastapi import status
from exceptions.custom_exceptions import (
    AppException,
    BadRequestException,
    NotFoundException,
)
from schemas.common_response import CommonResponseDTO
from schemas.module.module_request import ModuleRequestDTO
from repositories.module.module_repository import ModuleRepository
import mapper.module.module_mapper as module_mapper
from models.module.module import Module
from services.module.module_service import ModuleService

logger = logging.getLogger(__name__)


class ModuleServiceImpl(ModuleService):

    def __init__(self):
        self.module_repository = ModuleRepository()

    def create_or_update_module(
        self, db: Session, module_data: ModuleRequestDTO
    ) -> CommonResponseDTO:
        logger.info("ModuleServiceImpl => create_or_update_module: %s", module_data)

        # Check unique constraint on moduleName
        existing_module = self.module_repository.find_by_name(
            db, module_data.moduleName
        )
        if existing_module and (
            not module_data.moduleId or existing_module.id != module_data.moduleId
        ):
            raise BadRequestException(
                f"Module name '{module_data.moduleName}' already exists"
            )

        message = None
        module_entity: Module = None

        if module_data.moduleId and module_data.moduleId != null:
            module_entity = self.module_repository.find_by_id(db, module_data.moduleId)
            if not module_entity:
                raise NotFoundException(
                    f"Module with ID {module_data.moduleId} not found"
                )
            message = "Module updated successfully"
        else:
            module_entity = Module()
            message = "Module created successfully"

        try:
            module_entity = self.module_repository.create(
                db, module_mapper.to_model(module_entity, module_data)
            )
        except Exception as e:
            logger.error("Error creating/updating module: %s", e)
            raise AppException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Failed to create or update module, Please contact support",
            )

        return CommonResponseDTO(
            status=status.HTTP_201_CREATED,
            message=message,
            data=module_mapper.to_dto(module_entity),
        )

    def get_module_by_id(self, db: Session, module_id: int) -> CommonResponseDTO:
        logger.info("ModuleServiceImpl => get_module_by_id: %s", module_id)
        module_entity = self.module_repository.find_by_id(db, module_id)
        if not module_entity:
            raise NotFoundException(f"Module with ID {module_id} not found")

        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="Module retrieved successfully",
            data=module_mapper.to_dto(module_entity),
        )

    def delete_module_by_id(self, db: Session, module_id: int) -> CommonResponseDTO:
        logger.info("ModuleServiceImpl => delete_module_by_id: %s", module_id)
        module_entity = self.module_repository.find_by_id(db, module_id)
        if not module_entity:
            raise NotFoundException(f"Module with ID {module_id} not found")

        self.module_repository.delete(db, module_entity)

        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="Module deleted successfully",
            data=None,
        )

    def search_modules(
        self,
        db: Session,
        page: int,
        size: int,
        query: str,
        realm_id: int = None,
        application_id: int = None,
        active: bool = None,
    ) -> CommonResponseDTO:
        logger.info(
            "ModuleServiceImpl => search_modules: query=%s, realm_id=%s, application_id=%s, active=%s",
            query,
            realm_id,
            application_id,
            active,
        )
        modules, total_pages, total = self.module_repository.search(
            db, page, size, query, realm_id, application_id, active
        )
        module_dtos = module_mapper.to_dto_list(modules)

        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="Modules retrieved successfully",
            data={
                "modules": module_dtos,
                "total": total,
                "page": page,
                "size": size,
                "totalPages": total_pages,
            },
        )

    def get_all_active_modules(self, db: Session) -> CommonResponseDTO:
        logger.info("ModuleServiceImpl => get_all_active_modules")
        modules = self.module_repository.get_all_active_modules(db)
        module_dtos = module_mapper.to_dto_list(modules)

        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="Active modules retrieved successfully",
            data=module_dtos,
        )
