from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO
from schemas.auth.auth_request import TokenRequestDTO


class AuthService(ABC):

    @abstractmethod
    def get_token(
        self, db: Session, request_data: TokenRequestDTO
    ) -> CommonResponseDTO:
        pass
