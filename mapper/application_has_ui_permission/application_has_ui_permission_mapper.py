from schemas.application_has_ui_permission.application_has_ui_permission_request import (
    ApplicationHasUiPermissionRequestDTO,
)
from schemas.application_has_ui_permission.application_has_ui_permission_response import (
    ApplicationHasUiPermissionResponseDTO,
)
from models.application_has_ui_permission.application_has_ui_permission import (
    ApplicationHasUiPermission,
)
from mapper.realm.realm_mapper import to_dto as to_realm_dto
from mapper.application.application_mapper import to_application_dto
from mapper.ui_permission.ui_permission_mapper import to_dto as to_ui_permission_dto


def to_dto(
    mapping: ApplicationHasUiPermission,
) -> ApplicationHasUiPermissionResponseDTO:
    if not mapping:
        return None
    dto = ApplicationHasUiPermissionResponseDTO()
    dto.id = mapping.id
    dto.realmId = mapping.realmId
    dto.applicationId = mapping.applicationId
    dto.uiPermissionId = mapping.uiPermissionId
    dto.realm = to_realm_dto(mapping.realm) if mapping.realm else None
    dto.application = (
        to_application_dto(mapping.application) if mapping.application else None
    )
    dto.uiPermission = (
        to_ui_permission_dto(mapping.ui_permission)
        if mapping.ui_permission
        else None
    )
    return dto


def to_dto_list(mappings) -> list[ApplicationHasUiPermissionResponseDTO]:
    return [to_dto(m) for m in mappings]


def to_model(
    realm_id: int, application_id: int, ui_permission_id: int
) -> ApplicationHasUiPermission:
    mapping = ApplicationHasUiPermission()
    mapping.realmId = realm_id
    mapping.applicationId = application_id
    mapping.uiPermissionId = ui_permission_id
    return mapping
