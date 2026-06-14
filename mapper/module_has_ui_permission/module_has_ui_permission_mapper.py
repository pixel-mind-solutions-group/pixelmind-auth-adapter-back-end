from schemas.module_has_ui_permission.module_has_ui_permission_response import (
    ModuleHasUiPermissionResponseDTO,
)
from models.module_has_ui_permission.module_has_ui_permission import (
    ModuleHasUiPermission,
)
from mapper.module.module_mapper import to_dto as to_module_dto
from mapper.ui_permission.ui_permission_mapper import to_dto as to_ui_permission_dto


def to_dto(
    mapping: ModuleHasUiPermission,
) -> ModuleHasUiPermissionResponseDTO:
    if not mapping:
        return None
    dto = ModuleHasUiPermissionResponseDTO()
    dto.id = mapping.id
    dto.moduleId = mapping.moduleId
    dto.uiPermissionId = mapping.uiPermissionId
    dto.module = to_module_dto(mapping.module) if mapping.module else None
    dto.uiPermission = (
        to_ui_permission_dto(mapping.ui_permission)
        if mapping.ui_permission
        else None
    )
    return dto


def to_dto_list(mappings) -> list[ModuleHasUiPermissionResponseDTO]:
    return [to_dto(m) for m in mappings]


def to_model(
    module_id: int, ui_permission_id: int
) -> ModuleHasUiPermission:
    mapping = ModuleHasUiPermission()
    mapping.moduleId = module_id
    mapping.uiPermissionId = ui_permission_id
    return mapping
