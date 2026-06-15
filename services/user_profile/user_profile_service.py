from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO
from schemas.user_profile.user_profile_request import UserProfileRequestDTO


class UserProfileService(ABC):

    @abstractmethod
    def create_or_update_profile(
        self, db: Session, req_data: UserProfileRequestDTO
    ) -> CommonResponseDTO:
        pass

    @abstractmethod
    def get_profile_by_id(self, db: Session, profile_id: int) -> CommonResponseDTO:
        pass

    @abstractmethod
    def delete_profile_by_id(self, db: Session, profile_id: int) -> CommonResponseDTO:
        pass

    @abstractmethod
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
        pass
