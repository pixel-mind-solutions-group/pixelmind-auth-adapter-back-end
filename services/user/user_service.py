from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO
from schemas.user.user_request import UserRequestDTO


class UserService(ABC):

    @abstractmethod
    def create_or_update_user(self, db: Session, user_data: UserRequestDTO) -> CommonResponseDTO:
        pass

    @abstractmethod
    def get_user_by_id(self, db: Session, user_id: int) -> CommonResponseDTO:
        pass

    @abstractmethod
    def delete_user_by_id(self, db: Session, user_id: int) -> CommonResponseDTO:
        pass

    @abstractmethod
    def search_users(self, db: Session, page: int, size: int, query: str) -> CommonResponseDTO:
        pass
