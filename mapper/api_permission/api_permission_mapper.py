from schemas.api_permission.api_permission_request import ApiPermissionRequestDTO
from schemas.api_permission.api_permission_response import ApiPermissionResponseDTO
from models.api_permission.api_permission import ApiPermission


def to_dto(perm: ApiPermission) -> ApiPermissionResponseDTO:
    dto = ApiPermissionResponseDTO()
    dto.apiPermissionId = perm.id
    dto.apiPermissionName = perm.apiPermissionName
    dto.description = perm.description
    dto.active = perm.active
    dto.createdBy = perm.createdBy
    dto.createdAt = perm.createdAt.date().isoformat() if perm.createdAt else None
    return dto


def to_dto_list(perms) -> list[ApiPermissionResponseDTO]:
    return [to_dto(p) for p in perms]


def to_model(perm: ApiPermission, req: ApiPermissionRequestDTO) -> ApiPermission:
    perm.apiPermissionName = req.apiPermissionName
    perm.description = req.description
    perm.active = req.active
    return perm
