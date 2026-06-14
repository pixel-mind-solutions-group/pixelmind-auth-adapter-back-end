from schemas.module_has_api_permission.module_has_api_permission_response import (
    ModuleHasApiPermissionResponseDTO,
)
from models.module_has_api_permission.module_has_api_permission import (
    ModuleHasApiPermission,
)
from mapper.module.module_mapper import to_dto as to_module_dto
from mapper.api_permission.api_permission_mapper import to_dto as to_api_permission_dto


def to_dto(
    mapping: ModuleHasApiPermission,
) -> ModuleHasApiPermissionResponseDTO:
    if not mapping:
        return None
    dto = ModuleHasApiPermissionResponseDTO()
    dto.id = mapping.id
    dto.moduleId = mapping.moduleId
    dto.apiPermissionId = mapping.apiPermissionId
    dto.module = to_module_dto(mapping.module) if mapping.module else None
    dto.apiPermission = (
        to_api_permission_dto(mapping.api_permission)
        if mapping.api_permission
        else None
    )
    return dto


def to_dto_list(mappings) -> list[ModuleHasApiPermissionResponseDTO]:
    return [to_dto(m) for m in mappings]


def to_model(
    module_id: int, api_permission_id: int
) -> ModuleHasApiPermission:
    mapping = ModuleHasApiPermission()
    mapping.moduleId = module_id
    mapping.apiPermissionId = api_permission_id
    return mapping
