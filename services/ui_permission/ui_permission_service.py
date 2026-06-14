from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO
from schemas.ui_permission.ui_permission_request import UiPermissionRequestDTO


class UiPermissionService(ABC):

    @abstractmethod
    def create_or_update_permission(
        self, db: Session, req_data: UiPermissionRequestDTO
    ) -> CommonResponseDTO:
        pass

    @abstractmethod
    def get_permission_by_id(self, db: Session, perm_id: int) -> CommonResponseDTO:
        pass

    @abstractmethod
    def delete_permission_by_id(self, db: Session, perm_id: int) -> CommonResponseDTO:
        pass

    @abstractmethod
    def search_permissions(
        self,
        db: Session,
        page: int,
        size: int,
        query: str,
        active: bool = None,
    ) -> CommonResponseDTO:
        pass

    @abstractmethod
    def get_all_active_permissions(
        self,
        db: Session,
        realm_id: int,
        application_id: int,
        ui_permission_name: str = None,
    ) -> CommonResponseDTO:
        pass
