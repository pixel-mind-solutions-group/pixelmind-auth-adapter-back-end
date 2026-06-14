from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO
from schemas.user_role.user_role_request import UserRoleRequestDTO


class UserRoleService(ABC):

    @abstractmethod
    def create_or_update_role(
        self, db: Session, req_data: UserRoleRequestDTO
    ) -> CommonResponseDTO:
        pass

    @abstractmethod
    def get_role_by_id(self, db: Session, role_id: int) -> CommonResponseDTO:
        pass

    @abstractmethod
    def delete_role_by_id(self, db: Session, role_id: int) -> CommonResponseDTO:
        pass

    @abstractmethod
    def search_roles(
        self,
        db: Session,
        page: int,
        size: int,
        query: str = None,
        active: bool = None,
        realm_id: int = None,
        application_id: int = None,
    ) -> CommonResponseDTO:
        pass

    @abstractmethod
    def get_all_active_roles(
        self,
        db: Session,
        realm_id: int = None,
        application_id: int = None,
    ) -> CommonResponseDTO:
        pass
