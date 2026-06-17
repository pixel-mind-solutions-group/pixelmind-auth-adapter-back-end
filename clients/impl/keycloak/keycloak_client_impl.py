import logging
import urllib.request
import json
from clients.keycloak.keycloak_client import KeycloakClient
from core.settings import settings
from exceptions.custom_exceptions import KeycloakIntegrationException

logger = logging.getLogger(__name__)


class KeycloakClientImpl(KeycloakClient):

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
        except Exception as e:
            logger.error(f"Error fetching from keycloak adapter: {str(e)}")
            raise KeycloakIntegrationException(
                f"Keycloak adapter service unavailable: {str(e)}"
            )

        logger.info(
            "KeycloakClientImpl => get_active_realms_and_clients completed successfully"
        )
        return res_body.get("data", [])
