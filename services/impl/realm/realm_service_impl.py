import logging
from fastapi import status
from sqlalchemy.orm import Session
from schemas.common_response import CommonResponseDTO
from repositories.realm.realm_repository import RealmRepository
import mapper.realm.realm_mapper as realm_mapper
from services.realm.realm_service import RealmService
from models.realm.realm import Realm
from models.application.application import Application
from models.realms_has_applications.realms_has_applications import RealmsHasApplications
from clients.keycloak.keycloak_client import KeycloakClient
from core.dependancies.clients.client_dependency import get_keycloak_client
from exceptions.custom_exceptions import KeycloakIntegrationException

logger = logging.getLogger(__name__)


class RealmServiceImpl(RealmService):

    def __init__(self, keycloak_client: KeycloakClient = None):
        self.realm_repository = RealmRepository()
        self.keycloak_client = keycloak_client or get_keycloak_client()

    def sync_realms_and_applications(self, db: Session) -> CommonResponseDTO:
        logger.info(
            "RealmServiceImpl => sync_realms_and_applications function accessed"
        )

        # 1. Fetch active realms and clients from keycloak-adapter-backend
        try:
            keycloak_realms = self.keycloak_client.get_active_realms_and_clients()
        except KeycloakIntegrationException as e:
            return CommonResponseDTO(
                status=e.status_code,
                message=e.message,
                data=None,
            )

        if not isinstance(keycloak_realms, list):
            keycloak_realms = []

        try:
            # 2. Save active realms
            saved_realms = self.save_realm_list(db, keycloak_realms)

            # Map saved realms by internal_uuid to get the Realm object
            realm_map = {r.internal_uuid: r for r in saved_realms}

            # 3. Save clients/applications for each realm
            from core.dependancies.services.service_dependancy import (
                get_application_service,
            )

            app_service = get_application_service()
            all_active_client_uuids = set()
            for realm_data in keycloak_realms:
                internal_uuid = realm_data.get("id")
                realm_obj = realm_map.get(internal_uuid)
                if realm_obj:
                    clients_data = realm_data.get("clients", [])
                    app_service.save_client_list_while_sync(db, realm_obj, clients_data)
                    
                    if realm_obj.active:
                        for client_data in clients_data:
                            client_uuid = client_data.get("id")
                            client_active = client_data.get("active", True)
                            if client_uuid and client_active:
                                all_active_client_uuids.add(client_uuid)

            # Deactivate any applications not active across all synced realms
            app_service.deactivate_inactive_applications(db, list(all_active_client_uuids))

            db.commit()
        except Exception as e:
            db.rollback()
            logger.error(f"Error saving synced realms and clients: {str(e)}")
            return CommonResponseDTO(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"Failed to sync realms and clients: {str(e)}",
                data=None,
            )

        logger.info("RealmServiceImpl => sync_realms_and_applications function ended")
        return CommonResponseDTO(
            status=status.HTTP_200_OK,
            message="Realms and applications synchronized successfully",
            data=None,
        )

    def save_realm_list(self, db: Session, keycloak_realms: list) -> list[Realm]:
        logger.info("RealmServiceImpl => save_realm_list function accessed")
        saved_realms = []
        active_realm_ids = set()

        for realm_data in keycloak_realms:
            internal_uuid = realm_data.get("id")
            realm_name = realm_data.get("realmName")
            is_active = realm_data.get("enabled", True)

            if not internal_uuid or not realm_name:
                continue

            existing_realm = (
                db.query(Realm).filter(Realm.internal_uuid == internal_uuid).first()
            )
            if existing_realm:
                existing_realm.realm = realm_name
                existing_realm.active = is_active
                realm_obj = existing_realm
            else:
                realm_obj = Realm(
                    realm=realm_name, internal_uuid=internal_uuid, active=is_active
                )
                db.add(realm_obj)
                db.flush()

            saved_realms.append(realm_obj)
            active_realm_ids.add(realm_obj.id)

        # Deactivate other realms not present in Keycloak's sync list
        if active_realm_ids:
            db.query(Realm).filter(Realm.id.not_in(active_realm_ids)).update(
                {Realm.active: False}, synchronize_session=False
            )

        db.flush()
        return saved_realms

    def get_all_active_realms(self, db: Session) -> CommonResponseDTO:
        logger.info("RealmServiceImpl => get_all_active_realms function accessed")
        try:
            realms = self.realm_repository.get_all_active_realms(db)
            realm_dtos = realm_mapper.to_dto_list(realms)
            logger.info(
                "RealmServiceImpl => get_all_active_realms function ended successfully"
            )
            return CommonResponseDTO(
                status=status.HTTP_200_OK,
                message="Active realms retrieved successfully",
                data=realm_dtos,
            )
        except Exception as e:
            logger.error(f"Error fetching active realms: {str(e)}")
            return CommonResponseDTO(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"Failed to fetch active realms: {str(e)}",
                data=None,
            )
