from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO
from schemas.user_role_has_modules.user_role_has_modules_request import (
    UserRoleHasModulesRequestDTO,
)


class UserRoleHasModulesService(ABC):

    @abstractmethod
    def create_profile(
        self, db: Session, req_data: UserRoleHasModulesRequestDTO
    ) -> CommonResponseDTO:
        pass

    @abstractmethod
    def delete_profile_by_id(self, db: Session, mapping_id: int) -> CommonResponseDTO:
        pass

    @abstractmethod
    def search_assigned_profiles(
        self,
        db: Session,
        realm_id: int = None,
        application_id: int = None,
    ) -> CommonResponseDTO:
        pass
