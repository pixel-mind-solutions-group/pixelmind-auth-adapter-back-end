from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO


class RealmService(ABC):

    @abstractmethod
    def get_all_active_realms(self, db: Session) -> CommonResponseDTO:
        pass
