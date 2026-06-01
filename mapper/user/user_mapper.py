from schemas.user.user_request import UserRequestDTO
from schemas.user.user_response import UserResponseDTO
from models.user.user import User
from datetime import datetime


def to_dto(user: User) -> UserResponseDTO:
    dto = UserResponseDTO()
    dto.userId = user.id
    dto.email = user.email
    dto.firstName = user.firstName
    dto.lastName = user.lastName
    dto.username = user.username
    dto.active = user.active
    dto.emailVerified = user.emailVerified
    dto.failCount = user.failCount
    return dto


def to_dto_list(users) -> list[UserResponseDTO]:
    return [to_dto(user) for user in users]


def to_model(user: User, user_request: UserRequestDTO):

    user.email = user_request.email
    user.firstName = user_request.firstName
    user.lastName = user_request.lastName
    user.username = user_request.username
    user.active = user_request.active
    user.emailVerified = user_request.emailVerified
    user.createdBy = "system"
    user.createdAt = datetime.now()

    return user
