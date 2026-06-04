from schemas.application.application_response import ApplicationResponseDTO
from models.application.application import Application


def to_dto(application: Application) -> ApplicationResponseDTO:
    dto = ApplicationResponseDTO()
    dto.applicationId = application.id
    dto.applicationName = application.applicationName
    dto.active = application.active
    dto.uuid = application.uuid
    dto.realm = application.realm
    return dto


def to_dto_list(applications) -> list[ApplicationResponseDTO]:
    return [to_dto(application) for application in applications]
