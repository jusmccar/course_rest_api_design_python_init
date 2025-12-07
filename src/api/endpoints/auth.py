from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import authenticate
from ninja import Router

from api.schemas.auth_schemas import RefreshTokenRequestSchemaIn
from api.schemas.auth_schemas import TokenRequestSchemaIn
from api.schemas.auth_schemas import TokenRequestSchemaOut
from api.schemas.common_schemas import ErrorSchemaOut
from common.auth.jwt_auth import create_jwt
from core.models import AuthTokenModel

router = Router()


@router.post("/token/", response={200: TokenRequestSchemaOut, 401: ErrorSchemaOut}, auth=None)
def get_token(request, credentials: TokenRequestSchemaIn):
    """
    Token endpoint that returns a token.
    """
    user = authenticate(username=credentials.username, password=credentials.password)

    if not user:
        return (401, {"error": "Invalid credentials"})

    AuthTokenModel.objects.filter(user=user).delete()
    access_token = AuthTokenModel.objects.create(user=user, token_type=AuthTokenModel.TOKEN_TYPE_ACCESS)
    refresh_token = AuthTokenModel.objects.create(user=user, token_type=AuthTokenModel.TOKEN_TYPE_REFRESH)
    expires_in = int((access_token.expires - timezone.now()).total_seconds())

    return (200, {"access_token": access_token.key, "refresh_token": refresh_token.key, "expires_in": expires_in})

@router.post("/token/refresh/", response={200: TokenRequestSchemaOut, 401: ErrorSchemaOut}, auth=None)
def refresh_token(request, credentials: RefreshTokenRequestSchemaIn):
    """
    Token endpoint that refreshes a token.
    """
    obj = AuthTokenModel.objects.filter(key=credentials.refresh_token, token_type=AuthTokenModel.TOKEN_TYPE_REFRESH, is_active=True).first()

    if not obj:
        return (401, {"error": "Invalid refresh token"})

    if obj.is_expired():
        return (401, {"error": "Expired refresh token"})

    AuthTokenModel.objects.filter(user=obj.user).delete()
    access_token = AuthTokenModel.objects.create(user=obj.user, token_type=AuthTokenModel.TOKEN_TYPE_ACCESS)
    refresh_token = AuthTokenModel.objects.create(user=obj.user, token_type=AuthTokenModel.TOKEN_TYPE_REFRESH)
    expires_in = int((access_token.expires - timezone.now()).total_seconds())

    return (200, {"access_token": access_token.key, "refresh_token": refresh_token.key, "expires_in": expires_in})

@router.post("/jwt-token/", response={200: TokenRequestSchemaOut, 401: ErrorSchemaOut}, auth=None)
def get_jwt_token(request, credentials: TokenRequestSchemaIn):
    """
    JWT token endpoint that returns a JWT token.
    """
    user = authenticate(username=credentials.username, password=credentials.password)

    if not user:
        return (401, {"error": "Invalid credentials"})

    access_token = create_jwt(user_id=user.id, token_type=AuthTokenModel.TOKEN_TYPE_ACCESS)
    refresh_token = create_jwt(user_id=user.id, token_type=AuthTokenModel.TOKEN_TYPE_REFRESH)
    expires_in = int(timedelta(hours=4).total_seconds())

    return (200, {"access_token": access_token, "refresh_token": refresh_token, "expires_in": expires_in})
