from schemas.application_has_api_permission.application_has_api_permission_request import (
    ApplicationHasApiPermissionRequestDTO,
)
from schemas.application_has_api_permission.application_has_api_permission_response import (
    ApplicationHasApiPermissionResponseDTO,
)
from models.application_has_api_permission.application_has_api_permission import (
    ApplicationHasApiPermission,
)
from mapper.realm.realm_mapper import to_dto as to_realm_dto
from mapper.application.application_mapper import to_application_dto
from mapper.api_permission.api_permission_mapper import to_dto as to_api_permission_dto


def to_dto(
    mapping: ApplicationHasApiPermission,
) -> ApplicationHasApiPermissionResponseDTO:
    if not mapping:
        return None
    dto = ApplicationHasApiPermissionResponseDTO()
    dto.id = mapping.id
    dto.realmId = mapping.realmId
    dto.applicationId = mapping.applicationId
    dto.apiPermissionId = mapping.apiPermissionId
    dto.realm = to_realm_dto(mapping.realm) if mapping.realm else None
    dto.application = (
        to_application_dto(mapping.application) if mapping.application else None
    )
    dto.apiPermission = (
        to_api_permission_dto(mapping.api_permission)
        if mapping.api_permission
        else None
    )
    return dto


def to_dto_list(mappings) -> list[ApplicationHasApiPermissionResponseDTO]:
    return [to_dto(m) for m in mappings]


def to_model(
    realm_id: int, application_id: int, api_permission_id: int
) -> ApplicationHasApiPermission:
    mapping = ApplicationHasApiPermission()
    mapping.realmId = realm_id
    mapping.applicationId = application_id
    mapping.apiPermissionId = api_permission_id
    return mapping
