from schemas.application.application_response import ApplicationResponseDTO
from models.application.application import Application
from mapper.realm.realm_mapper import to_dto as to_realm_dto


def to_dto(application: Application) -> ApplicationResponseDTO:
    dto = ApplicationResponseDTO()
    dto.id =    application.id
    dto.clientId = application.clientId
    dto.uuid = application.uuid
    dto.active = application.active
    dto.realm = to_realm_dto(application.realm) if application.realm else None
    return dto


def to_dto_list(applications) -> list[ApplicationResponseDTO]:
    return [to_dto(application) for application in applications]
