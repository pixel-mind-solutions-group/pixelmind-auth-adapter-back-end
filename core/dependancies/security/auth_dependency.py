from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from exceptions.custom_exceptions import UnauthorizedException

http_bearer = HTTPBearer(auto_error=False)


def get_token_from_header(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> str:
    """
    Extracts the Bearer access token from the HTTP Authorization header.

    Raises:
        UnauthorizedException: If the header is missing, malformed, or empty.
    """
    if not credentials or not credentials.credentials:
        raise UnauthorizedException("Missing or invalid Authorization Bearer header")

    token = credentials.credentials.strip()
    if token.lower().startswith("bearer "):
        token = token[7:].strip()
    token = token.strip('"').strip("'").strip()

    if not token:
        raise UnauthorizedException("Empty Authorization token")

    return token

