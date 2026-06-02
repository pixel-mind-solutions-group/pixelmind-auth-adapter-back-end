from datetime import datetime
import logging

from fastapi import status
from sqlalchemy import null
from sqlalchemy.orm import Session
from exceptions.custom_exceptions import (
    AppException,
    BadRequestException,
    NotFoundException,
)

# schema model imports
from schemas.common_response import CommonResponseDTO
from schemas.user.user_request import UserRequestDTO

# repository imports
from repositories.user.user_repository import UserRepository as UserRepository

# mapper imports
import mapper.user.user_mapper as user_mapper

# model imports
from models.user.user import User

logger = logging.getLogger(__name__)


class UserService:

    def __init__(self):
        self.user_repository = UserRepository()

    def create_or_update_user(self, db: Session, user_data: UserRequestDTO):

        logger.info(
            "UserService => create_or_update_user function accessed: %s", user_data
        )

        message = None
        user_entity: User = None

        if user_data.userId and user_data.userId != null:
            user_entity = self.user_repository.find_by_id(db, user_data.userId)

            if not user_entity:
                raise BadRequestException(f"User with ID {user_data.userId} not found")

            user_entity.updatedAt = datetime.now()
            user_entity.updatedBy = "system"
            message = "User updated successfully"

        else:
            user_entity = User()
            user_entity.failCount = 0
            user_entity.createdAt = datetime.now()
            user_entity.createdBy = "system"
            message = "User created successfully"

        try:

            user_entity = self.user_repository.create(
                db, user_mapper.to_model(user_entity, user_data)
            )

        except Exception as e:
            logger.error("Error creating/updating user: %s", e)

            raise AppException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Failed to create or update user, Please contact support",
            )

        logger.info(
            "UserService => create_or_update_user function ended: %s", user_data
        )

        return CommonResponseDTO(
            status=status.HTTP_201_CREATED,
            message=message,
            data=user_mapper.to_dto(user_entity),
        )

    def get_user_by_id(self, db: Session, user_id: int):
        logger.info("UserService => get_user_by_id function accessed: %s", user_id)

        user_entity = self.user_repository.find_by_id(db, user_id)

        if not user_entity:
            raise NotFoundException(f"User with ID {user_id} not found")

        logger.info("UserService => get_user_by_id function ended: %s", user_id)

        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="User retrieved successfully",
            data=user_mapper.to_dto(user_entity),
        )

    def delete_user_by_id(self, db: Session, user_id: int):
        logger.info("UserService => delete_user_by_id function accessed: %s", user_id)

        user_entity = self.user_repository.find_by_id(db, user_id)

        if not user_entity:
            raise NotFoundException(f"User with ID {user_id} not found")

        self.user_repository.delete(db, user_entity)

        logger.info("UserService => delete_user_by_id function ended: %s", user_id)

        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="User deleted successfully",
            data=None,
        )

    def search_users(self, db: Session, page: int, size: int, query: str):

        logger.info("UserService => search_users function accessed: %s", query)

        users, total_pages, total = self.user_repository.search(db, page, size, query)

        user_dtos = user_mapper.to_dto_list(users)

        logger.info("UserService => search_users function ended: %s", query)

        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="Users retrieved response",
            data={
                "users": user_dtos,
                "total": total,
                "page": page,
                "size": size,
                "totalPages": total_pages,
            },
        )
