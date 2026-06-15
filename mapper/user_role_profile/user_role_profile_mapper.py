from schemas.user_role_profile.user_role_has_modules_has_api_permission_response import (
    UserRoleHasModulesHasApiPermissionResponseDTO,
)
from schemas.user_role_profile.user_role_has_modules_has_ui_permission_response import (
    UserRoleHasModulesHasUiPermissionResponseDTO,
)
from models.user_role_has_modules_has_api_permission.user_role_has_modules_has_api_permission import (
    UserRoleHasModulesHasApiPermission,
)
from models.user_role_has_modules_has_ui_permission.user_role_has_modules_has_ui_permission import (
    UserRoleHasModulesHasUiPermission,
)
from mapper.realm.realm_mapper import to_dto as to_realm_dto
from mapper.application.application_mapper import to_application_dto
from mapper.user_role.user_role_mapper import to_dto as to_user_role_dto
from mapper.module.module_mapper import to_dto as to_module_dto
from mapper.api_permission.api_permission_mapper import to_dto as to_api_perm_dto
from mapper.ui_permission.ui_permission_mapper import to_dto as to_ui_perm_dto


def to_api_dto(
    mapping: UserRoleHasModulesHasApiPermission,
) -> UserRoleHasModulesHasApiPermissionResponseDTO:
    if not mapping:
        return None
    dto = UserRoleHasModulesHasApiPermissionResponseDTO()
    dto.id = mapping.id
    dto.realmId = mapping.realmId
    dto.applicationId = mapping.applicationId
    dto.userRoleId = mapping.userRoleId
    dto.moduleId = mapping.moduleId
    dto.apiPermissionId = mapping.apiPermissionId

    dto.realm = to_realm_dto(mapping.realm) if mapping.realm else None
    dto.application = (
        to_application_dto(mapping.application) if mapping.application else None
    )
    dto.userRole = to_user_role_dto(mapping.user_role) if mapping.user_role else None
    dto.module = to_module_dto(mapping.module) if mapping.module else None
    dto.apiPermission = (
        to_api_perm_dto(mapping.api_permission) if mapping.api_permission else None
    )
    return dto


def to_api_dto_list(mappings) -> list[UserRoleHasModulesHasApiPermissionResponseDTO]:
    return [to_api_dto(m) for m in mappings]


def to_api_model(
    realm_id: int,
    application_id: int,
    role_id: int,
    module_id: int = None,
    api_permission_id: int = None,
) -> UserRoleHasModulesHasApiPermission:
    mapping = UserRoleHasModulesHasApiPermission()
    mapping.realmId = realm_id
    mapping.applicationId = application_id
    mapping.userRoleId = role_id
    mapping.moduleId = module_id
    mapping.apiPermissionId = api_permission_id
    return mapping


def to_ui_dto(
    mapping: UserRoleHasModulesHasUiPermission,
) -> UserRoleHasModulesHasUiPermissionResponseDTO:
    if not mapping:
        return None
    dto = UserRoleHasModulesHasUiPermissionResponseDTO()
    dto.id = mapping.id
    dto.realmId = mapping.realmId
    dto.applicationId = mapping.applicationId
    dto.userRoleId = mapping.userRoleId
    dto.moduleId = mapping.moduleId
    dto.uiPermissionId = mapping.uiPermissionId

    dto.realm = to_realm_dto(mapping.realm) if mapping.realm else None
    dto.application = (
        to_application_dto(mapping.application) if mapping.application else None
    )
    dto.userRole = to_user_role_dto(mapping.user_role) if mapping.user_role else None
    dto.module = to_module_dto(mapping.module) if mapping.module else None
    dto.uiPermission = (
        to_ui_perm_dto(mapping.ui_permission) if mapping.ui_permission else None
    )
    return dto


def to_ui_dto_list(mappings) -> list[UserRoleHasModulesHasUiPermissionResponseDTO]:
    return [to_ui_dto(m) for m in mappings]


def to_ui_model(
    realm_id: int,
    application_id: int,
    role_id: int,
    module_id: int = None,
    ui_permission_id: int = None,
) -> UserRoleHasModulesHasUiPermission:
    mapping = UserRoleHasModulesHasUiPermission()
    mapping.realmId = realm_id
    mapping.applicationId = application_id
    mapping.userRoleId = role_id
    mapping.moduleId = module_id
    mapping.uiPermissionId = ui_permission_id
    return mapping
