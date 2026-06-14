from schemas.ui_permission.ui_permission_request import UiPermissionRequestDTO
from schemas.ui_permission.ui_permission_response import UiPermissionResponseDTO
from models.ui_permission.ui_permission import UiPermission


def to_dto(perm: UiPermission) -> UiPermissionResponseDTO:
    dto = UiPermissionResponseDTO()
    dto.uiPermissionId = perm.id
    dto.uiPermissionName = perm.uiPermissionName
    dto.description = perm.description
    dto.active = perm.active
    dto.createdBy = perm.createdBy
    dto.createdAt = perm.createdAt.date().isoformat() if perm.createdAt else None
    return dto


def to_dto_list(perms) -> list[UiPermissionResponseDTO]:
    return [to_dto(p) for p in perms]


def to_model(perm: UiPermission, req: UiPermissionRequestDTO) -> UiPermission:
    perm.uiPermissionName = req.uiPermissionName
    perm.description = req.description
    perm.active = req.active
    return perm
