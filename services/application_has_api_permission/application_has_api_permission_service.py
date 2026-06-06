from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO
from schemas.application_has_api_permission.application_has_api_permission_request import (
    ApplicationHasApiPermissionRequestDTO,
)


class ApplicationHasApiPermissionService(ABC):

    @abstractmethod
    def create_profile(
        self, db: Session, req_data: ApplicationHasApiPermissionRequestDTO
    ) -> CommonResponseDTO:
        pass

    @abstractmethod
    def delete_profile_by_id(self, db: Session, mapping_id: int) -> CommonResponseDTO:
        pass
