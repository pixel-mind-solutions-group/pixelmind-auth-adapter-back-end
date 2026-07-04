from schemas.application.application_response import ApplicationResponseDTO
from models.realms_has_applications.realms_has_applications import RealmsHasApplications
from models.application.application import Application
from mapper.realm.realm_mapper import to_dto as to_realm_dto


def to_dto(mapping: RealmsHasApplications) -> ApplicationResponseDTO:
    dto = ApplicationResponseDTO()
    if mapping and mapping.application:
        dto.id = mapping.application.id
        dto.clientId = mapping.application.clientId
    else:
        dto.id = None
        dto.clientId = None
    dto.active = mapping.active if mapping else None
    dto.uuid = mapping.uuid if mapping else None
    dto.internalApplicationUuid = mapping.internal_application_uuid if mapping else None
    dto.realm = to_realm_dto(mapping.realm) if mapping and mapping.realm else None
    return dto


def to_dto_list(mappings) -> list[ApplicationResponseDTO]:
    return [to_dto(mapping) for mapping in mappings]


def to_application_dto(application: Application) -> ApplicationResponseDTO:
    if not application:
        return None
    dto = ApplicationResponseDTO()
    dto.id = application.id
    dto.clientId = application.clientId
    dto.active = application.active
    return dto
