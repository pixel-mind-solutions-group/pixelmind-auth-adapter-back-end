import logging
import urllib.request
import urllib.error
import json
from clients.keycloak.keycloak_client import KeycloakClient
from core.settings import settings
from exceptions.custom_exceptions import KeycloakIntegrationException

logger = logging.getLogger(__name__)


class KeycloakClientImpl(KeycloakClient):

    def _handle_http_error(self, e: urllib.error.HTTPError, action_desc: str) -> None:
        try:
            res_body = json.loads(e.read().decode("utf-8"))
            msg = res_body.get("errorDescription") or res_body.get("message") or res_body.get("error") or str(e)
        except Exception:
            msg = str(e)
        logger.error(f"Error {action_desc}: {msg}")
        raise KeycloakIntegrationException(msg)

    def get_active_realms_and_clients(self) -> list:
        logger.info("KeycloakClientImpl => get_active_realms_and_clients accessed")
        url = f"{settings.KEYCLOAK_ADAPTER_URL}/realm/active"
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status != 200:
                    logger.error(
                        f"Keycloak adapter returned status code {response.status}"
                    )
                    raise KeycloakIntegrationException(
                        f"Failed to fetch realms from Keycloak adapter. Status: {response.status}"
                    )

                res_body = json.loads(response.read().decode("utf-8"))
        except KeycloakIntegrationException:
            raise
        except urllib.error.HTTPError as e:
            self._handle_http_error(e, "fetching from keycloak adapter")
        except Exception as e:
            logger.error(f"Error fetching from keycloak adapter: {str(e)}")
            raise KeycloakIntegrationException(
                f"Keycloak adapter service unavailable: {str(e)}"
            )

        logger.info(
            "KeycloakClientImpl => get_active_realms_and_clients completed successfully"
        )
        return res_body.get("data", [])

    def create_api_permissions(
        self,
        realm_internal_uuid: str,
        internal_app_uuid: str,
        permission_names: list[str],
    ) -> None:
        logger.info(
            "KeycloakClientImpl => create_api_permissions accessed. realm: %s, app: %s",
            realm_internal_uuid,
            internal_app_uuid,
        )
        url = f"{settings.KEYCLOAK_ADAPTER_URL}/client/api-permissions/create"
        payload = {
            "realmInternalUUid": realm_internal_uuid,
            "internalApplicationUuid": internal_app_uuid,
            "apiPermisisonName": permission_names,
        }
        try:
            req_data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=req_data,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status not in (200, 201):
                    logger.error(
                        f"Keycloak adapter returned status code {response.status}"
                    )
                    raise KeycloakIntegrationException(
                        f"Failed to register API permissions in Keycloak. Status: {response.status}"
                    )

                res_body = json.loads(response.read().decode("utf-8"))
                if res_body.get("status") not in (200, 201):
                    msg = res_body.get("message", "Unknown error")
                    logger.error(f"Keycloak adapter returned failure in body: {msg}")
                    raise KeycloakIntegrationException(
                        f"Failed to register API permissions in Keycloak: {msg}"
                    )
        except KeycloakIntegrationException:
            raise
        except urllib.error.HTTPError as e:
            self._handle_http_error(e, "calling Keycloak adapter to register permissions")
        except Exception as e:
            logger.error(
                f"Error calling Keycloak adapter to register permissions: {str(e)}"
            )
            raise KeycloakIntegrationException(
                f"Keycloak adapter service unavailable: {str(e)}"
            )

        logger.info(
            "KeycloakClientImpl => create_api_permissions completed successfully"
        )

    def create_realm_role(self, realm_name: str, role_name: str, description: str = None) -> None:
        logger.info(
            "KeycloakClientImpl => create_realm_role: realm: %s, role: %s",
            realm_name,
            role_name
        )
        url = f"{settings.KEYCLOAK_ADAPTER_URL}/role/realm/create"
        payload = {
            "realmName": realm_name,
            "name": role_name,
            "description": description
        }
        try:
            req_data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=req_data,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status not in (200, 201):
                    raise KeycloakIntegrationException(
                        f"Failed to create realm role in Keycloak. Status: {response.status}"
                    )
                res_body = json.loads(response.read().decode("utf-8"))
                if res_body.get("status") not in (200, 201):
                    msg = res_body.get("message", "Unknown error")
                    raise KeycloakIntegrationException(
                        f"Failed to create realm role in Keycloak: {msg}"
                    )
        except KeycloakIntegrationException:
            raise
        except urllib.error.HTTPError as e:
            self._handle_http_error(e, "creating realm role in Keycloak adapter")
        except Exception as e:
            logger.error("Error creating realm role in Keycloak adapter: %s", e)
            raise KeycloakIntegrationException(
                f"Keycloak adapter service unavailable: {str(e)}"
            )

    def update_realm_role(self, realm_name: str, old_role_name: str, new_role_name: str, description: str = None) -> None:
        logger.info(
            "KeycloakClientImpl => update_realm_role: realm: %s, oldRole: %s, newRole: %s",
            realm_name,
            old_role_name,
            new_role_name
        )
        url = f"{settings.KEYCLOAK_ADAPTER_URL}/role/realm/update"
        payload = {
            "realmName": realm_name,
            "name": old_role_name,
            "newName": new_role_name,
            "description": description
        }
        try:
            req_data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=req_data,
                headers={"Content-Type": "application/json"},
                method="PUT",
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status not in (200, 201):
                    raise KeycloakIntegrationException(
                        f"Failed to update realm role in Keycloak. Status: {response.status}"
                    )
                res_body = json.loads(response.read().decode("utf-8"))
                if res_body.get("status") not in (200, 201):
                    msg = res_body.get("message", "Unknown error")
                    raise KeycloakIntegrationException(
                        f"Failed to update realm role in Keycloak: {msg}"
                    )
        except KeycloakIntegrationException:
            raise
        except urllib.error.HTTPError as e:
            self._handle_http_error(e, "updating realm role in Keycloak adapter")
        except Exception as e:
            logger.error("Error updating realm role in Keycloak adapter: %s", e)
            raise KeycloakIntegrationException(
                f"Keycloak adapter service unavailable: {str(e)}"
            )

    def delete_realm_role(self, realm_name: str, role_name: str) -> None:
        logger.info(
            "KeycloakClientImpl => delete_realm_role: realm: %s, role: %s",
            realm_name,
            role_name
        )
        import urllib.parse
        encoded_realm = urllib.parse.quote(realm_name)
        encoded_role = urllib.parse.quote(role_name)
        url = f"{settings.KEYCLOAK_ADAPTER_URL}/role/realm/delete?realmName={encoded_realm}&roleName={encoded_role}"
        try:
            req = urllib.request.Request(
                url,
                method="DELETE",
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status not in (200, 201):
                    raise KeycloakIntegrationException(
                        f"Failed to delete realm role in Keycloak. Status: {response.status}"
                    )
                res_body = json.loads(response.read().decode("utf-8"))
                if res_body.get("status") not in (200, 201):
                    msg = res_body.get("message", "Unknown error")
                    raise KeycloakIntegrationException(
                        f"Failed to delete realm role in Keycloak: {msg}"
                    )
        except KeycloakIntegrationException:
            raise
        except urllib.error.HTTPError as e:
            self._handle_http_error(e, "deleting realm role in Keycloak adapter")
        except Exception as e:
            logger.error("Error deleting realm role in Keycloak adapter: %s", e)
            raise KeycloakIntegrationException(
                f"Keycloak adapter service unavailable: {str(e)}"
            )

    def delete_api_permission(
        self,
        realm_internal_uuid: str,
        internal_app_uuid: str,
        permission_name: str,
    ) -> None:
        logger.info(
            "KeycloakClientImpl => delete_api_permission accessed. realm: %s, app: %s, permission: %s",
            realm_internal_uuid,
            internal_app_uuid,
            permission_name,
        )
        import urllib.parse
        encoded_realm_uuid = urllib.parse.quote(realm_internal_uuid)
        encoded_app_uuid = urllib.parse.quote(internal_app_uuid)
        encoded_perm_name = urllib.parse.quote(permission_name)
        url = f"{settings.KEYCLOAK_ADAPTER_URL}/client/api-permissions/delete?realmInternalUUid={encoded_realm_uuid}&internalApplicationUuid={encoded_app_uuid}&apiPermissionName={encoded_perm_name}"
        try:
            req = urllib.request.Request(
                url,
                method="DELETE",
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status not in (200, 201):
                    logger.error(
                        f"Keycloak adapter returned status code {response.status}"
                    )
                    raise KeycloakIntegrationException(
                        f"Failed to delete API permission in Keycloak. Status: {response.status}"
                    )

                res_body = json.loads(response.read().decode("utf-8"))
                if res_body.get("status") not in (200, 201):
                    msg = res_body.get("message", "Unknown error")
                    logger.error(f"Keycloak adapter returned failure in body: {msg}")
                    raise KeycloakIntegrationException(
                        f"Failed to delete API permission in Keycloak: {msg}"
                    )
        except KeycloakIntegrationException:
            raise
        except urllib.error.HTTPError as e:
            self._handle_http_error(e, "calling Keycloak adapter to delete permission")
        except Exception as e:
            logger.error(
                f"Error calling Keycloak adapter to delete permission: {str(e)}"
            )
            raise KeycloakIntegrationException(
                f"Keycloak adapter service unavailable: {str(e)}"
            )

        logger.info(
            "KeycloakClientImpl => delete_api_permission completed successfully"
        )

    def sync_user(self, realm_name: str, user_data: dict) -> None:
        logger.info(
            "KeycloakClientImpl => sync_user accessed. realm: %s, user: %s",
            realm_name,
            user_data.get("username"),
        )
        import urllib.parse
        encoded_realm = urllib.parse.quote(realm_name)
        url = f"{settings.KEYCLOAK_ADAPTER_URL}/user/sync?realmName={encoded_realm}"
        try:
            req_data = json.dumps(user_data).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=req_data,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status not in (200, 201):
                    logger.error(
                        f"Keycloak adapter returned status code {response.status}"
                    )
                    raise KeycloakIntegrationException(
                        f"Failed to sync user in Keycloak. Status: {response.status}"
                    )

                res_body = json.loads(response.read().decode("utf-8"))
                if res_body.get("status") not in (200, 201):
                    msg = res_body.get("message", "Unknown error")
                    logger.error(f"Keycloak adapter returned failure in body: {msg}")
                    raise KeycloakIntegrationException(
                        f"Failed to sync user in Keycloak: {msg}"
                    )
        except KeycloakIntegrationException:
            raise
        except urllib.error.HTTPError as e:
            self._handle_http_error(e, "calling Keycloak adapter to sync user")
        except Exception as e:
            logger.error("Error calling Keycloak adapter to sync user: %s", e)
            raise KeycloakIntegrationException(
                f"Keycloak adapter service unavailable: {str(e)}"
            )

        logger.info("KeycloakClientImpl => sync_user completed successfully")

    def assign_user_permissions(
        self,
        realm_name: str,
        username: str,
        client_id: str,
        permissions: list[str],
    ) -> None:
        logger.info(
            "KeycloakClientImpl => assign_user_permissions accessed. realm: %s, user: %s, client: %s",
            realm_name,
            username,
            client_id,
        )
        url = f"{settings.KEYCLOAK_ADAPTER_URL}/user/assign-permissions"
        payload = {
            "realmName": realm_name,
            "username": username,
            "clientId": client_id,
            "permissions": permissions,
        }
        try:
            req_data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=req_data,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status not in (200, 201):
                    logger.error(
                        f"Keycloak adapter returned status code {response.status}"
                    )
                    raise KeycloakIntegrationException(
                        f"Failed to assign user permissions in Keycloak. Status: {response.status}"
                    )

                res_body = json.loads(response.read().decode("utf-8"))
                if res_body.get("status") not in (200, 201):
                    msg = res_body.get("message", "Unknown error")
                    logger.error(f"Keycloak adapter returned failure in body: {msg}")
                    raise KeycloakIntegrationException(
                        f"Failed to assign user permissions in Keycloak: {msg}"
                    )
        except KeycloakIntegrationException:
            raise
        except urllib.error.HTTPError as e:
            self._handle_http_error(e, "calling Keycloak adapter to assign user permissions")
        except Exception as e:
            logger.error(
                f"Error calling Keycloak adapter to assign user permissions: {str(e)}"
            )
            raise KeycloakIntegrationException(
                f"Keycloak adapter service unavailable: {str(e)}"
            )

        logger.info(
            "KeycloakClientImpl => assign_user_permissions completed successfully"
        )


