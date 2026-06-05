from schemas.realm.realm_response import RealmResponseDTO
from models.realm.realm import Realm


def to_dto(realm: Realm) -> RealmResponseDTO:
    dto = RealmResponseDTO()
    dto.id = realm.id
    dto.realm = realm.realm
    dto.uuid = realm.uuid
    dto.active = realm.active
    return dto


def to_dto_list(realms) -> list[RealmResponseDTO]:
    return [to_dto(r) for r in realms]
