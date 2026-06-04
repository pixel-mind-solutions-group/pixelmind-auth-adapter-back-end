from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO


class ApplicationService(ABC):

    @abstractmethod
    def search_applications(
        self, db: Session, page: int, size: int, query: str
    ) -> CommonResponseDTO:
        pass
