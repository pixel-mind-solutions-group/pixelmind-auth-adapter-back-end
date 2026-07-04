import logging
from sqlalchemy.orm import Session
from services.auth.auth_service import AuthService
from schemas.common_response import CommonResponseDTO
from schemas.auth.auth_request import TokenRequestDTO
from models.realms_has_applications.realms_has_applications import RealmsHasApplications
from clients.impl.keycloak.keycloak_client_impl import KeycloakClientImpl
from exceptions.custom_exceptions import NotFoundException, BadRequestException
from fastapi import status

logger = logging.getLogger(__name__)


class AuthServiceImpl(AuthService):

    def __init__(self):
        self.keycloak_client = KeycloakClientImpl()

    def get_token(
        self, db: Session, request_data: TokenRequestDTO
    ) -> CommonResponseDTO:
        logger.info(
            "AuthServiceImpl => get_token accessed for user: %s, app_uuid: %s",
            request_data.username,
            request_data.application_uuid,
        )

        # 1. Fetch application mapping from database
        mapping = (
            db.query(RealmsHasApplications)
            .filter(RealmsHasApplications.uuid == request_data.application_uuid)
            .first()
        )

        if not mapping:
            raise NotFoundException(
                f"Application mapping with UUID {request_data.application_uuid} not found"
            )

        if not mapping.active or not mapping.application.active or not mapping.realm.active:
            raise BadRequestException("The requested application or realm is inactive")

        realm_name = mapping.realm.realm
        internal_app_uuid = mapping.internal_application_uuid

        # 2. Call Keycloak client implementation to get tokens
        token_data = self.keycloak_client.get_token(
            realm_name=realm_name,
            internal_app_uuid=internal_app_uuid,
            username=request_data.username,
            password=request_data.password,
        )

        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            data=token_data,
            message="Tokens retrieved successfully",
        )
