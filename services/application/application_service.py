from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO


class ApplicationService(ABC):

    @abstractmethod
    def get_all_applications(self, db: Session) -> CommonResponseDTO:
        pass
