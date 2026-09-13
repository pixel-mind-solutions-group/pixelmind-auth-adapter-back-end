from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO


class RealmService(ABC):

    @abstractmethod
    def sync_realms_and_applications(self, db: Session) -> CommonResponseDTO:
        pass

    @abstractmethod
    def save_realm_list(self, db: Session, keycloak_realms: list) -> list:
        pass

    @abstractmethod
    def get_all_active_realms(self, db: Session, only_active: bool = True) -> CommonResponseDTO:
        pass

    @abstractmethod
    def delete_realm(self, db: Session, realm_id: int) -> CommonResponseDTO:
        pass

    @abstractmethod
    def delete_by_realm_and_application(
        self, db: Session, realm_id: int, application_id: int
    ) -> CommonResponseDTO:
        pass
