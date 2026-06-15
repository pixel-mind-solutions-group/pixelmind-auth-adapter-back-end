import logging
from sqlalchemy import null
from sqlalchemy.orm import Session
from fastapi import status
from exceptions.custom_exceptions import (
    BadRequestException,
    NotFoundException,
    AppException,
)
from schemas.common_response import CommonResponseDTO
from schemas.user_profile.user_profile_request import UserProfileRequestDTO
from models.user_profile.user_profile import UserProfile
from models.realm.realm import Realm
from models.application.application import Application
from models.user_role.user_role import UserRole
from models.user.user import User
from repositories.user_profile.user_profile_repository import UserProfileRepository
from services.user_profile.user_profile_service import UserProfileService
import mapper.user_profile.user_profile_mapper as mapper

logger = logging.getLogger(__name__)


class UserProfileServiceImpl(UserProfileService):

    def __init__(self):
        self.repository = UserProfileRepository()

    def create_or_update_profile(
        self, db: Session, req_data: UserProfileRequestDTO
    ) -> CommonResponseDTO:
        logger.info("UserProfileServiceImpl => create_or_update_profile: %s", req_data)

        # 1. Verify Realm exists
        realm = db.query(Realm).filter(Realm.id == req_data.realmId).first()
        if not realm:
            raise NotFoundException(f"Realm with ID {req_data.realmId} not found")

        # 2. Verify Application exists
        app = db.query(Application).filter(Application.id == req_data.applicationId).first()
        if not app:
            raise NotFoundException(f"Application with ID {req_data.applicationId} not found")

        # 3. Verify User exists
        user = db.query(User).filter(User.id == req_data.userId).first()
        if not user:
            raise NotFoundException(f"User with ID {req_data.userId} not found")

        # 4. Verify UserRole exists and belongs to Realm/Application
        role = db.query(UserRole).filter(UserRole.id == req_data.userRoleId).first()
        if not role:
            raise NotFoundException(f"User Role with ID {req_data.userRoleId} not found")
        if role.realmId != req_data.realmId or role.applicationId != req_data.applicationId:
            raise BadRequestException(
                f"User Role with ID {req_data.userRoleId} does not belong to the selected Realm/Application"
            )

        message = None
        entity: UserProfile = None

        if req_data.id and req_data.id != null:
            entity = self.repository.find_by_id(db, req_data.id)
            if not entity:
                raise NotFoundException(f"User Profile mapping with ID {req_data.id} not found")

            # Check unique constraint for another entry
            existing = self.repository.find_by_composite(
                db, req_data.userId, req_data.realmId, req_data.applicationId, req_data.userRoleId
            )
            if existing and existing.id != req_data.id:
                raise BadRequestException("User profile mapping already exists")

            message = "User Profile updated successfully"
        else:
            # Check composite unique constraint
            existing = self.repository.find_by_composite(
                db, req_data.userId, req_data.realmId, req_data.applicationId, req_data.userRoleId
            )
            if existing:
                raise BadRequestException("User profile mapping already exists")

            entity = UserProfile()
            message = "User Profile mapped successfully"

        try:
            entity = self.repository.create(db, mapper.to_model(entity, req_data))
        except Exception as e:
            logger.error("Error creating/updating user profile: %s", e)
            raise AppException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Failed to save user profile mapping",
            )

        return CommonResponseDTO(
            status=status.HTTP_201_CREATED,
            message=message,
            data=mapper.to_dto(entity),
        )

    def get_profile_by_id(self, db: Session, profile_id: int) -> CommonResponseDTO:
        logger.info("UserProfileServiceImpl => get_profile_by_id: %s", profile_id)
        entity = self.repository.find_by_id(db, profile_id)
        if not entity:
            raise NotFoundException(f"User Profile mapping with ID {profile_id} not found")

        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="User Profile retrieved successfully",
            data=mapper.to_dto(entity),
        )

    def delete_profile_by_id(self, db: Session, profile_id: int) -> CommonResponseDTO:
        logger.info("UserProfileServiceImpl => delete_profile_by_id: %s", profile_id)
        entity = self.repository.find_by_id(db, profile_id)
        if not entity:
            raise NotFoundException(f"User Profile mapping with ID {profile_id} not found")

        self.repository.delete(db, entity)

        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="User Profile mapping deleted successfully",
            data=None,
        )

    def search_profiles(
        self,
        db: Session,
        page: int,
        size: int,
        realm_id: int = None,
        application_id: int = None,
        user_id: int = None,
        user_role_id: int = None,
        search_query: str = None,
    ) -> CommonResponseDTO:
        logger.info(
            "UserProfileServiceImpl => search_profiles: realm_id=%s, app_id=%s, user_id=%s, role_id=%s, search_query=%s",
            realm_id,
            application_id,
            user_id,
            user_role_id,
            search_query,
        )
        profiles, total_pages, total = self.repository.search(
            db, page, size, realm_id, application_id, user_id, user_role_id, search_query
        )
        dtos = mapper.to_dto_list(profiles)

        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="User profiles retrieved successfully",
            data={
                "profiles": dtos,
                "total": total,
                "page": page,
                "size": size,
                "totalPages": total_pages,
            },
        )
