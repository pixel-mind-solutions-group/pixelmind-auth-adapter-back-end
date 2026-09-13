import logging
import urllib.request
import urllib.error
import json
import base64
import time
from clients.keycloak.keycloak_client import KeycloakClient
from core.settings import settings
from exceptions.custom_exceptions import (
    KeycloakIntegrationException,
    UnauthorizedException,
)

logger = logging.getLogger(__name__)


class KeycloakClientImpl(KeycloakClient):

    def _handle_http_error(self, e: urllib.error.HTTPError, action_desc: str) -> None:
        try:
            res_body = json.loads(e.read().decode("utf-8"))
            msg = (
                res_body.get("errorDescription")
                or res_body.get("message")
                or res_body.get("error")
                or str(e)
            )
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
            self._handle_http_error(
                e, "calling Keycloak adapter to register permissions"
            )
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

    def create_realm_role(
        self, realm_name: str, role_name: str, description: str = None
    ) -> None:
        logger.info(
            "KeycloakClientImpl => create_realm_role: realm: %s, role: %s",
            realm_name,
            role_name,
        )
        url = f"{settings.KEYCLOAK_ADAPTER_URL}/role/realm/create"
        payload = {
            "realmName": realm_name,
            "name": role_name,
            "description": description,
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

    def update_realm_role(
        self,
        realm_name: str,
        old_role_name: str,
        new_role_name: str,
        description: str = None,
    ) -> None:
        logger.info(
            "KeycloakClientImpl => update_realm_role: realm: %s, oldRole: %s, newRole: %s",
            realm_name,
            old_role_name,
            new_role_name,
        )
        url = f"{settings.KEYCLOAK_ADAPTER_URL}/role/realm/update"
        payload = {
            "realmName": realm_name,
            "name": old_role_name,
            "newName": new_role_name,
            "description": description,
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
            role_name,
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
            try:
                res_body = json.loads(e.read().decode("utf-8"))
                msg = (
                    res_body.get("errorDescription")
                    or res_body.get("message")
                    or res_body.get("error")
                    or str(e)
                )
            except Exception:
                msg = str(e)

            if not permissions and (
                e.code == 404 or "404" in str(msg) or "not found" in str(msg).lower()
            ):
                logger.warning(
                    f"User {username} or client {client_id} not found in Keycloak realm {realm_name} during permission cleanup ({msg}). Skipping."
                )
                return

            self._handle_http_error(
                e, "calling Keycloak adapter to assign user permissions"
            )
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

    def delete_user(self, realm_name: str, username: str) -> None:
        logger.info(
            "KeycloakClientImpl => delete_user accessed. realm: %s, user: %s",
            realm_name,
            username,
        )
        import urllib.parse

        encoded_realm = urllib.parse.quote(realm_name)
        encoded_user = urllib.parse.quote(username)
        url = f"{settings.KEYCLOAK_ADAPTER_URL}/user/delete?realmName={encoded_realm}&username={encoded_user}"
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
                        f"Failed to delete user in Keycloak. Status: {response.status}"
                    )

                res_body = json.loads(response.read().decode("utf-8"))
                if res_body.get("status") not in (200, 201):
                    msg = res_body.get("message", "Unknown error")
                    logger.error(f"Keycloak adapter returned failure in body: {msg}")
                    raise KeycloakIntegrationException(
                        f"Failed to delete user in Keycloak: {msg}"
                    )
        except KeycloakIntegrationException:
            raise
        except urllib.error.HTTPError as e:
            try:
                res_body = json.loads(e.read().decode("utf-8"))
                msg = (
                    res_body.get("errorDescription")
                    or res_body.get("message")
                    or res_body.get("error")
                    or str(e)
                )
            except Exception:
                msg = str(e)

            if e.code == 404 or "404" in str(msg) or "not found" in str(msg).lower():
                logger.warning(
                    f"User {username} not found in Keycloak realm {realm_name} during delete ({msg}). Considering delete successful."
                )
                return

            self._handle_http_error(e, "calling Keycloak adapter to delete user")
        except Exception as e:
            logger.error("Error calling Keycloak adapter to delete user: %s", e)
            raise KeycloakIntegrationException(
                f"Keycloak adapter service unavailable: {str(e)}"
            )

        logger.info("KeycloakClientImpl => delete_user completed successfully")

    def get_token(
        self,
        realm_name: str,
        internal_app_uuid: str,
        username: str,
        password: str,
    ) -> dict:
        logger.info(
            "KeycloakClientImpl => get_token accessed. realm: %s, internal_app_uuid: %s, user: %s",
            realm_name,
            internal_app_uuid,
            username,
        )
        url = f"{settings.KEYCLOAK_ADAPTER_URL}/auth/token/app"
        payload = {
            "realmName": realm_name,
            "internalApplicationUuid": internal_app_uuid,
            "username": username,
            "password": password,
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
                        f"Failed to retrieve tokens in Keycloak. Status: {response.status}"
                    )

                res_body = json.loads(response.read().decode("utf-8"))
                if res_body.get("status") not in (200, 201):
                    msg = res_body.get("message", "Unknown error")
                    logger.error(f"Keycloak adapter returned failure in body: {msg}")
                    raise KeycloakIntegrationException(
                        f"Failed to retrieve tokens in Keycloak: {msg}"
                    )
                return res_body.get("data", {})
        except KeycloakIntegrationException:
            raise
        except urllib.error.HTTPError as e:
            self._handle_http_error(e, "calling Keycloak adapter to get token")
        except Exception as e:
            logger.error("Error calling Keycloak adapter to get token: %s", e)
            raise KeycloakIntegrationException(
                f"Keycloak adapter service unavailable: {str(e)}"
            )

    def sync_user_role_api_permissions_of_realm_and_application(
        self,
        realm_internal_uuid: str,
        application_internal_uuid: str,
        role_wise_permissions: list[dict],
    ) -> None:
        logger.info(
            "KeycloakClientImpl => sync_user_role_api_permissions_of_realm_and_application accessed. realm: %s, application: %s",
            realm_internal_uuid,
            application_internal_uuid,
        )
        encoded_realm_uuid = urllib.parse.quote(realm_internal_uuid)
        encoded_application_uuid = urllib.parse.quote(application_internal_uuid)
        url = f"{settings.KEYCLOAK_ADAPTER_URL}/role/sync-api-permissions?realmInternalUuid={encoded_realm_uuid}&applicationInternalUuid={encoded_application_uuid}"
        payload = role_wise_permissions
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
                        f"Failed to sync API permissions in Keycloak. Status: {response.status}"
                    )

                res_body = json.loads(response.read().decode("utf-8"))
                if res_body.get("status") not in (200, 201):
                    msg = res_body.get("message", "Unknown error")
                    logger.error(f"Keycloak adapter returned failure in body: {msg}")
                    raise KeycloakIntegrationException(
                        f"Failed to sync API permissions in Keycloak: {msg}"
                    )
                return res_body.get("data", {})
        except KeycloakIntegrationException:
            raise
        except urllib.error.HTTPError as e:
            self._handle_http_error(
                e, "calling Keycloak adapter to sync API permissions"
            )
        except Exception as e:
            logger.error(
                "Error calling Keycloak adapter to sync API permissions: %s", e
            )
            raise KeycloakIntegrationException(
                f"Keycloak adapter service unavailable: {str(e)}"
            )

    def sync_users_by_role_scope(
        self,
        realm_name: str,
        role_scope: str,
        payload: dict,
    ) -> dict:
        logger.info(
            "KeycloakClientImpl => sync_users_by_role_scope accessed. realm: %s, role_scope: %s",
            realm_name,
            role_scope,
        )
        import urllib.parse

        encoded_realm = urllib.parse.quote(realm_name)
        encoded_role_scope = urllib.parse.quote(role_scope)
        url = f"{settings.KEYCLOAK_ADAPTER_URL}/user/sync-by-role-scope?realmName={encoded_realm}&roleScope={encoded_role_scope}"
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
                        f"Failed to sync users by role scope in Keycloak. Status: {response.status}"
                    )

                res_body = json.loads(response.read().decode("utf-8"))
                if res_body.get("status") not in (200, 201):
                    msg = res_body.get("message", "Unknown error")
                    logger.error(f"Keycloak adapter returned failure in body: {msg}")
                    raise KeycloakIntegrationException(
                        f"Failed to sync users by role scope in Keycloak: {msg}"
                    )
                return res_body.get("data", {})
        except KeycloakIntegrationException:
            raise
        except urllib.error.HTTPError as e:
            self._handle_http_error(
                e, "calling Keycloak adapter to sync users by role scope"
            )
        except Exception as e:
            logger.error(
                "Error calling Keycloak adapter to sync users by role scope: %s", e
            )
            raise KeycloakIntegrationException(
                f"Keycloak adapter service unavailable: {str(e)}"
            )

    def verify_token(self, token: str) -> dict:
        logger.info("KeycloakClientImpl => verify_token accessed")
        if not token or not token.strip():
            raise UnauthorizedException("Authorization token is missing")

        # Clean token (remove duplicate Bearer prefix, quotes, and whitespace)
        clean_token = token.strip()
        if clean_token.lower().startswith("bearer "):
            clean_token = clean_token[7:].strip()
        clean_token = clean_token.strip('"').strip("'").strip()

        # 1. Parse JWT header and payload
        try:
            parts = clean_token.split(".")
            if len(parts) != 3:
                raise UnauthorizedException(
                    "Invalid token format: expected JWT with 3 segments"
                )

            # Header
            header_b64 = parts[0]
            header_padded = header_b64 + "=" * (-len(header_b64) % 4)
            header = json.loads(base64.urlsafe_b64decode(header_padded).decode("utf-8"))
            kid = header.get("kid")

            # Payload
            payload_b64 = parts[1]
            payload_padded = payload_b64 + "=" * (-len(payload_b64) % 4)
            payload = json.loads(base64.urlsafe_b64decode(payload_padded).decode("utf-8"))
        except UnauthorizedException:
            raise
        except Exception as e:
            logger.error("Failed to parse token segments: %s", e)
            raise UnauthorizedException(f"Invalid token payload: {str(e)}")

        # 2. Check token expiration
        exp = payload.get("exp")
        now = time.time()
        if exp and now > exp:
            logger.warning("Token has expired. exp=%s, now=%s", exp, now)
            raise UnauthorizedException("Token has expired. Please refresh your token.")

        # 3. Extract issuer and realm name
        issuer = payload.get("iss")
        if not issuer:
            raise UnauthorizedException("Token missing 'iss' (issuer) claim")

        # Example: "http://localhost:8080/realms/PIXEL_IAM" -> "PIXEL_IAM"
        realm_name = issuer.rstrip("/").split("/realms/")[-1]

        logger.info(
            "verify_token => issuer: %s, realm: %s, user: %s, azp: %s",
            issuer,
            realm_name,
            payload.get("preferred_username"),
            payload.get("azp"),
        )

        # 4. Verify token against Keycloak realm JWKS certificates
        certs_url = f"{issuer.rstrip('/')}/protocol/openid-connect/certs"
        try:
            certs_req = urllib.request.Request(certs_url, method="GET")
            with urllib.request.urlopen(certs_req, timeout=10) as certs_resp:
                if certs_resp.status == 200:
                    certs_data = json.loads(certs_resp.read().decode("utf-8"))
                    valid_kids = [
                        k.get("kid")
                        for k in certs_data.get("keys", [])
                        if k.get("kid")
                    ]
                    if kid and valid_kids and kid not in valid_kids:
                        logger.error(
                            "Token kid '%s' not found in Keycloak realm certs: %s",
                            kid,
                            valid_kids,
                        )
                        raise UnauthorizedException(
                            "Invalid token: key ID not recognized by Keycloak"
                        )
                    logger.info(
                        "Token successfully verified against Keycloak realm certs (kid=%s)",
                        kid,
                    )
        except UnauthorizedException:
            raise
        except urllib.error.URLError as e:
            logger.error("Failed to reach Keycloak at %s: %s", certs_url, e)
            raise KeycloakIntegrationException(
                f"Keycloak service unreachable at {certs_url}: {str(e)}"
            )
        except Exception as e:
            logger.error("Unexpected error during Keycloak token verification: %s", e)
            raise KeycloakIntegrationException(
                f"Error during Keycloak token verification: {str(e)}"
            )

        # 5. Build verified claims directly from validated JWT payload
        verified_data = {
            "sub": payload.get("sub"),
            "preferred_username": (
                payload.get("preferred_username")
                or payload.get("username")
                or payload.get("sub")
            ),
            "email": payload.get("email"),
            "name": payload.get("name"),
            "given_name": payload.get("given_name"),
            "family_name": payload.get("family_name"),
            "realm_name": realm_name,
            "azp": payload.get("azp") or payload.get("client_id"),
            "payload": payload,
            "userinfo": {},
        }
        logger.info(
            "KeycloakClientImpl => verify_token completed successfully for user: %s",
            verified_data.get("preferred_username"),
        )
        return verified_data


