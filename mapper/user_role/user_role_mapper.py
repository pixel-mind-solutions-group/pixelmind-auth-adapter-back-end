from schemas.user_role.user_role_request import UserRoleRequestDTO
from schemas.user_role.user_role_response import UserRoleResponseDTO
from models.user_role.user_role import UserRole
from mapper.realm.realm_mapper import to_dto as to_realm_dto
from mapper.application.application_mapper import to_application_dto


def to_dto(role: UserRole) -> UserRoleResponseDTO:
    if not role:
        return None
    dto = UserRoleResponseDTO()
    dto.roleId = role.id
    dto.realmId = role.realmId
    dto.applicationId = role.applicationId
    dto.roleName = role.roleName
    dto.description = role.description
    dto.active = role.active

    dto.realm = to_realm_dto(role.realm) if role.realm else None
    dto.application = to_application_dto(role.application) if role.application else None
    return dto


def to_dto_list(roles) -> list[UserRoleResponseDTO]:
    return [to_dto(r) for r in roles]


def to_model(role: UserRole, req: UserRoleRequestDTO) -> UserRole:
    role.realmId = req.realmId
    role.applicationId = req.applicationId
    role.roleName = req.roleName
    role.description = req.description
    role.active = req.active
    return role
