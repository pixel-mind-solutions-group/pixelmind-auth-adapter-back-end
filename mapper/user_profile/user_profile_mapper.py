from schemas.user_profile.user_profile_response import UserProfileResponseDTO
from schemas.user_profile.user_profile_request import UserProfileRequestDTO
from models.user_profile.user_profile import UserProfile
from mapper.user.user_mapper import to_dto as to_user_dto
from mapper.realm.realm_mapper import to_dto as to_realm_dto
from mapper.application.application_mapper import to_application_dto
from mapper.user_role.user_role_mapper import to_dto as to_user_role_dto


def to_dto(model: UserProfile) -> UserProfileResponseDTO:
    if not model:
        return None
    dto = UserProfileResponseDTO()
    dto.id = model.id
    dto.userId = model.userId
    dto.realmId = model.realmId
    dto.applicationId = model.applicationId
    dto.userRoleId = model.userRoleId

    dto.user = to_user_dto(model.user) if model.user else None
    dto.realm = to_realm_dto(model.realm) if model.realm else None
    dto.application = to_application_dto(model.application) if model.application else None
    dto.userRole = to_user_role_dto(model.user_role) if model.user_role else None
    return dto


def to_dto_list(models: list[UserProfile]) -> list[UserProfileResponseDTO]:
    return [to_dto(m) for m in models]


def to_model(entity: UserProfile, dto: UserProfileRequestDTO) -> UserProfile:
    entity.userId = dto.userId
    entity.realmId = dto.realmId
    entity.applicationId = dto.applicationId
    entity.userRoleId = dto.userRoleId
    return entity
