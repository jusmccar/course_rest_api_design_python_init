from datetime import timedelta

from django.contrib.auth import authenticate
from django.utils import timezone

from api.logic.exceptions import AuthenticationError
from api.logic.exceptions import TokenExpiredError
from api.logic.exceptions import TokenInvalidError
from common.auth.jwt_auth import create_jwt
from core.models import AuthTokenModel


def handle_get_token(username: str, password: str) -> dict:
    user = authenticate(username=username, password=password)

    if not user:
        raise AuthenticationError("Invalid credentials")

    AuthTokenModel.objects.filter(user=user).delete()
    access_token = AuthTokenModel.objects.create(user=user, token_type=AuthTokenModel.TOKEN_TYPE_ACCESS)
    refresh_token = AuthTokenModel.objects.create(user=user, token_type=AuthTokenModel.TOKEN_TYPE_REFRESH)
    expires_in = int((access_token.expires - timezone.now()).total_seconds())

    return {"access_token": access_token.key, "refresh_token": refresh_token.key, "expires_in": expires_in}


def handle_refresh_token(refresh_token: str) -> dict:
    token_obj = AuthTokenModel.objects.filter(key=refresh_token, token_type=AuthTokenModel.TOKEN_TYPE_REFRESH, is_active=True).first()

    if not token_obj:
        raise TokenInvalidError("Invalid refresh token")

    if token_obj.is_expired():
        raise TokenExpiredError("Expired refresh token")

    AuthTokenModel.objects.filter(user=token_obj.user).delete()
    access_token = AuthTokenModel.objects.create(user=token_obj.user, token_type=AuthTokenModel.TOKEN_TYPE_ACCESS)
    refresh_token = AuthTokenModel.objects.create(user=token_obj.user, token_type=AuthTokenModel.TOKEN_TYPE_REFRESH)
    expires_in = int((access_token.expires - timezone.now()).total_seconds())

    return {"access_token": access_token.key, "refresh_token": refresh_token.key, "expires_in": expires_in}


def handle_get_jwt_token(username: str, password: str) -> dict:
    user = authenticate(username=username, password=password)

    if not user:
        raise AuthenticationError("Invalid credentials")

    access_token = create_jwt(user_id=user.id, token_type=AuthTokenModel.TOKEN_TYPE_ACCESS)
    refresh_token = create_jwt(user_id=user.id, token_type=AuthTokenModel.TOKEN_TYPE_REFRESH)
    expires_in = int(timedelta(hours=4).total_seconds())

    return {"access_token": access_token, "refresh_token": refresh_token, "expires_in": expires_in}
