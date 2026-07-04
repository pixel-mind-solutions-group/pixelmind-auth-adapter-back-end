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

    @abstractmethod
    def create_api_permissions(
        self,
        realm_internal_uuid: str,
        internal_app_uuid: str,
        permission_names: list[str],
    ) -> None:
        """
        Creates API permissions (roles) in Keycloak via the Keycloak adapter backend.

        Args:
            realm_internal_uuid (str): The internal UUID of the realm.
            internal_app_uuid (str): The internal UUID of the client application.
            permission_names (list[str]): List of API permission names to register.

        Raises:
            KeycloakIntegrationException: If the call to Keycloak adapter fails.
        """
        pass

    @abstractmethod
    def create_realm_role(
        self, realm_name: str, role_name: str, description: str = None
    ) -> None:
        """
        Creates a realm role in Keycloak.
        """
        pass

    @abstractmethod
    def update_realm_role(
        self,
        realm_name: str,
        old_role_name: str,
        new_role_name: str,
        description: str = None,
    ) -> None:
        """
        Updates a realm role in Keycloak.
        """
        pass

    @abstractmethod
    def delete_realm_role(self, realm_name: str, role_name: str) -> None:
        """
        Deletes a realm role in Keycloak.
        """
        pass

    @abstractmethod
    def delete_api_permission(
        self,
        realm_internal_uuid: str,
        internal_app_uuid: str,
        permission_name: str,
    ) -> None:
        """
        Deletes an API permission (role) from Keycloak client.
        """
        pass
