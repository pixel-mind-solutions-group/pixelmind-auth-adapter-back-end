import logging
from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import status

from services.auth.auth_service import AuthService
from schemas.common_response import CommonResponseDTO
from schemas.auth.auth_request import TokenRequestDTO
from schemas.auth.user_details_response import UserDetailsResponseDTO
from models.user.user import User
from models.realm.realm import Realm
from models.application.application import Application
from models.user_profile.user_profile import UserProfile
from models.user_role_has_modules_has_ui_permission.user_role_has_modules_has_ui_permission import (
    UserRoleHasModulesHasUiPermission,
)
from models.ui_permission.ui_permission import UiPermission
from models.realms_has_applications.realms_has_applications import RealmsHasApplications
from clients.keycloak.keycloak_client import KeycloakClient
from clients.impl.keycloak.keycloak_client_impl import KeycloakClientImpl
from core.dependancies.clients.client_dependency import get_keycloak_client
from exceptions.custom_exceptions import (
    NotFoundException,
    BadRequestException,
    UnauthorizedException,
    ForbiddenException,
)

logger = logging.getLogger(__name__)


class AuthServiceImpl(AuthService):

    def __init__(self, keycloak_client: Optional[KeycloakClient] = None):
        self.keycloak_client: KeycloakClient = keycloak_client or get_keycloak_client()

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

    def get_user_details(
        self,
        db: Session,
        token: str,
        application_uuid: Optional[str] = None,
    ) -> CommonResponseDTO:
        logger.info("AuthServiceImpl => get_user_details accessed")

        # 1. Verify token with Keycloak (UserInfo endpoint / introspection)
        token_claims = self.keycloak_client.verify_token(token)
        username = (
            token_claims.get("preferred_username")
            or token_claims.get("username")
            or token_claims.get("sub")
        )
        if not username:
            raise UnauthorizedException(
                "Could not extract username from verified token claims"
            )

        # 2. Authorize user from local database
        user = db.query(User).filter(User.username == username).first()
        if not user:
            logger.warning(
                "User '%s' verified by Keycloak but not found in local database",
                username,
            )
            raise NotFoundException(f"User '{username}' not found in system")

        if not user.active:
            logger.warning("User '%s' account is inactive", username)
            raise ForbiddenException("User account is inactive")

        # 3. Determine Realm and Application scope
        realm = None
        application = None

        if application_uuid:
            mapping = (
                db.query(RealmsHasApplications)
                .filter(RealmsHasApplications.uuid == application_uuid)
                .first()
            )
            if not mapping:
                raise NotFoundException(
                    f"Application mapping with UUID {application_uuid} not found"
                )
            if (
                not mapping.active
                or not mapping.realm.active
                or not mapping.application.active
            ):
                raise BadRequestException(
                    "The requested realm or application is inactive"
                )
            realm = mapping.realm
            application = mapping.application
        else:
            # Resolve from token claims
            token_realm_name = token_claims.get("realm_name")
            token_client_id = token_claims.get("azp")

            if token_realm_name:
                realm = (
                    db.query(Realm)
                    .filter(Realm.realm == token_realm_name)
                    .first()
                )

            if token_client_id:
                application = (
                    db.query(Application)
                    .filter(Application.clientId == token_client_id)
                    .first()
                )

        # 4. Resolve User Profile and User Role
        profile_query = db.query(UserProfile).filter(UserProfile.userId == user.id)
        if realm:
            profile_query = profile_query.filter(UserProfile.realmId == realm.id)
        if application:
            profile_query = profile_query.filter(
                UserProfile.applicationId == application.id
            )

        user_profile = profile_query.first()

        role_name = None
        component_list: List[str] = []

        if user_profile and user_profile.user_role:
            role = user_profile.user_role
            role_name = role.roleName

            # 5. Fetch UI permissions (componentList) assigned to this user role
            ui_perms_query = (
                db.query(UiPermission.uiPermissionName)
                .join(
                    UserRoleHasModulesHasUiPermission,
                    UserRoleHasModulesHasUiPermission.uiPermissionId == UiPermission.id,
                )
                .filter(
                    UserRoleHasModulesHasUiPermission.userRoleId == role.id,
                    UiPermission.active == True,
                )
            )
            if realm:
                ui_perms_query = ui_perms_query.filter(
                    UserRoleHasModulesHasUiPermission.realmId == realm.id
                )
            if application:
                ui_perms_query = ui_perms_query.filter(
                    UserRoleHasModulesHasUiPermission.applicationId == application.id
                )

            ui_perms = ui_perms_query.all()
            component_list = sorted(
                list(set([name for (name,) in ui_perms if name]))
            )

        # 6. Build response DTO
        response_dto = UserDetailsResponseDTO(
            userId=user.id,
            username=user.username,
            email=user.email,
            firstName=user.firstName,
            lastName=user.lastName,
            realm=realm.realm if realm else token_claims.get("realm_name"),
            application=application.clientId if application else token_claims.get("azp"),
            role=role_name,
            componentList=component_list,
        )

        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="User details retrieved successfully",
            data=response_dto,
        )
