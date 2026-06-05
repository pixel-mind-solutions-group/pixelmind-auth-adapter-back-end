from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO


class ApplicationService(ABC):

    @abstractmethod
    def get_all_active_applications(self, db: Session) -> CommonResponseDTO:
        pass

    @abstractmethod
    def search_applications(
        self,
        db: Session,
        page: int,
        size: int,
        query: str = None,
        realm_id: int = None,
        application_id: int = None,
    ) -> CommonResponseDTO:
        pass
