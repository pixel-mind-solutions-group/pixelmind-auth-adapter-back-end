from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO
from schemas.module.module_request import ModuleRequestDTO


class ModuleService(ABC):

    @abstractmethod
    def create_or_update_module(
        self, db: Session, module_data: ModuleRequestDTO
    ) -> CommonResponseDTO:
        pass

    @abstractmethod
    def get_module_by_id(self, db: Session, module_id: int) -> CommonResponseDTO:
        pass

    @abstractmethod
    def delete_module_by_id(self, db: Session, module_id: int) -> CommonResponseDTO:
        pass

    @abstractmethod
    def search_modules(
        self,
        db: Session,
        page: int,
        size: int,
        query: str,
        realm_id: int = None,
        application_id: int = None,
        active: bool = None,
    ) -> CommonResponseDTO:
        pass

    @abstractmethod
    def get_all_active_modules(self, db: Session) -> CommonResponseDTO:
        pass
