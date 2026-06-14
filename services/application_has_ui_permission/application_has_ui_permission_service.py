from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO
from schemas.application_has_ui_permission.application_has_ui_permission_request import (
    ApplicationHasUiPermissionRequestDTO,
)


class ApplicationHasUiPermissionService(ABC):

    @abstractmethod
    def create_profile(
        self, db: Session, req_data: ApplicationHasUiPermissionRequestDTO
    ) -> CommonResponseDTO:
        pass

    @abstractmethod
    def delete_profile_by_id(self, db: Session, mapping_id: int) -> CommonResponseDTO:
        pass

    @abstractmethod
    def search_assigned_permissions(
        self,
        db: Session,
        realm_id: int = None,
        application_id: int = None,
        ui_permission_name: str = None,
    ) -> CommonResponseDTO:
        pass
