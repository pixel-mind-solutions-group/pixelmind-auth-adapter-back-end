from typing import Optional
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

    @abstractmethod
    def get_user_details(
        self,
        db: Session,
        token: str,
        application_uuid: Optional[str] = None,
    ) -> CommonResponseDTO:
        """
        Verifies access token with Keycloak, authorizes the user,
        and retrieves user details, role, and UI permissions (componentList).
        """
        pass

