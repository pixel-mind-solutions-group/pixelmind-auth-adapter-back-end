from clients.keycloak.keycloak_client import KeycloakClient
from clients.impl.keycloak.keycloak_client_impl import KeycloakClientImpl


def get_keycloak_client() -> KeycloakClient:
    return KeycloakClientImpl()
