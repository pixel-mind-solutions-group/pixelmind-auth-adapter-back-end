from abc import ABC, abstractmethod


class KeycloakClient(ABC):

    @abstractmethod
    def get_active_realms_and_clients(self) -> list:
        """
        Fetches active realms and their clients from the Keycloak adapter backend.

        Returns:
            list: List of active realms containing their details and associated client applications.

        Raises:
            KeycloakIntegrationException: If the call to Keycloak adapter fails.
        """
        pass
