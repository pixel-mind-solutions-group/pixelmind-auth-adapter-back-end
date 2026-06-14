from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO
from schemas.module_has_api_permission.module_has_api_permission_request import (
    ModuleHasApiPermissionRequestDTO,
)


class ModuleHasApiPermissionService(ABC):

    @abstractmethod
    def create_profile(
        self, db: Session, req_data: ModuleHasApiPermissionRequestDTO
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
        module_id: int = None,
        api_permission_name: str = None,
    ) -> CommonResponseDTO:
        pass
