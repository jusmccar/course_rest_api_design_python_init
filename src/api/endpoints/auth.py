from ninja import Router

from api.logic.auth_logic import handle_get_token
from api.logic.auth_logic import handle_get_jwt_token
from api.logic.auth_logic import handle_refresh_token
from api.logic.auth_logic import handle_refresh_jwt_token
from api.logic.exceptions import get_error_response
from api.schemas.auth_schemas import RefreshTokenRequestSchemaIn
from api.schemas.auth_schemas import TokenRequestSchemaIn
from api.schemas.auth_schemas import TokenRequestSchemaOut
from api.schemas.common_schemas import ErrorSchemaOut
from core.models import AuthTokenModel

router = Router()


@router.post("/token/", response={200: TokenRequestSchemaOut, 401: ErrorSchemaOut}, auth=None)
def get_token(request, credentials: TokenRequestSchemaIn):
    """
    Token endpoint that returns a token.
    """
    username = credentials.username
    password = credentials.password

    try:
        data = handle_get_token(username, password)
    except Exception as e:
        status_code, error_response = get_error_response(e)

        return (status_code, error_response)

    return (200, data)


@router.post("/token/refresh/", response={200: TokenRequestSchemaOut, 401: ErrorSchemaOut}, auth=None)
def refresh_token(request, credentials: RefreshTokenRequestSchemaIn):
    """
    Token endpoint that refreshes a token.
    """
    refresh_token = credentials.refresh_token

    try:
        data = handle_refresh_token(refresh_token)
    except Exception as e:
        status_code, error_response = get_error_response(e)

        return (status_code, error_response)

    return (200, data)


@router.post("/jwt-token/", response={200: TokenRequestSchemaOut, 401: ErrorSchemaOut}, auth=None)
def get_jwt_token(request, credentials: TokenRequestSchemaIn):
    """
    JWT token endpoint that returns a JWT token.
    """
    username = credentials.username
    password = credentials.password

    try:
        data = handle_get_jwt_token(username, password)
    except Exception as e:
        status_code, error_response = get_error_response(e)

        return (status_code, error_response)

    return (200, data)


@router.post("/jwt-token/refresh/", response={200: TokenRequestSchemaOut, 401: ErrorSchemaOut}, auth=None)
def refresh_jwt_token(request, credentials: RefreshTokenRequestSchemaIn):
    """
    JWT token endpoint that refreshes a JWT token.
    """
    refresh_token = credentials.refresh_token

    try:
        data = handle_refresh_jwt_token(refresh_token)
    except Exception as e:
        status_code, error_response = get_error_response(e)

        return (status_code, error_response)

    return (200, data)
