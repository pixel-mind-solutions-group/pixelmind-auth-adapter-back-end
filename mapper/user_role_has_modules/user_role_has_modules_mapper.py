from schemas.user_role_has_modules.user_role_has_modules_response import (
    UserRoleHasModulesResponseDTO,
)
from models.user_role_has_modules.user_role_has_modules import (
    UserRoleHasModules,
)
from mapper.realm.realm_mapper import to_dto as to_realm_dto
from mapper.application.application_mapper import to_application_dto
from mapper.user_role.user_role_mapper import to_dto as to_user_role_dto
from mapper.module.module_mapper import to_dto as to_module_dto


def to_dto(
    mapping: UserRoleHasModules,
) -> UserRoleHasModulesResponseDTO:
    if not mapping:
        return None
    dto = UserRoleHasModulesResponseDTO()
    dto.id = mapping.id
    dto.realmId = mapping.realmId
    dto.applicationId = mapping.applicationId
    dto.userRoleId = mapping.userRoleId
    dto.moduleId = mapping.moduleId

    dto.realm = to_realm_dto(mapping.realm) if mapping.realm else None
    dto.application = (
        to_application_dto(mapping.application) if mapping.application else None
    )
    dto.userRole = to_user_role_dto(mapping.user_role) if mapping.user_role else None
    dto.module = to_module_dto(mapping.module) if mapping.module else None
    return dto


def to_dto_list(mappings) -> list[UserRoleHasModulesResponseDTO]:
    return [to_dto(m) for m in mappings]


def to_model(
    realm_id: int, application_id: int, role_id: int, module_id: int = None
) -> UserRoleHasModules:
    mapping = UserRoleHasModules()
    mapping.realmId = realm_id
    mapping.applicationId = application_id
    mapping.userRoleId = role_id
    mapping.moduleId = module_id
    return mapping
