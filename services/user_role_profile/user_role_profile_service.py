from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO
from schemas.user_role_profile.user_role_profile_request import (
    UserRoleProfileRequestDTO,
)
from schemas.user_role_profile.user_role_profile_sync_request import (
    UserRoleProfileSyncRequestDTO,
)


class UserRoleProfileService(ABC):

    @abstractmethod
    def create_profile(
        self, db: Session, req_data: UserRoleProfileRequestDTO
    ) -> CommonResponseDTO:
        pass

    @abstractmethod
    def delete_api_profile_by_id(self, db: Session, mapping_id: int) -> CommonResponseDTO:
        pass

    @abstractmethod
    def delete_ui_profile_by_id(self, db: Session, mapping_id: int) -> CommonResponseDTO:
        pass

    @abstractmethod
    def search_assigned_profiles(
        self,
        db: Session,
        realm_id: int = None,
        application_id: int = None,
        user_role_id: int = None,
        module_id: int = None,
    ) -> CommonResponseDTO:
        pass

    @abstractmethod
    def sync_profile(
        self, db: Session, req_data: UserRoleProfileSyncRequestDTO
    ) -> CommonResponseDTO:
        pass
