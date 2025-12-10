from datetime import timedelta
import jwt

from django.conf import settings
from django.contrib.auth import authenticate
from django.utils import timezone

from api.logic.exceptions import AuthenticationError
from api.logic.exceptions import TokenExpiredError
from api.logic.exceptions import TokenInvalidError
from common.auth.jwt_auth import create_jwt
from core.models import AuthTokenModel
from core.models import DogUserModel


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


def handle_refresh_jwt_token(refresh_token: str) -> dict:
    try:
        data = jwt.decode(refresh_token, settings.JWT_SECRET, algorithms=["HS256"])
    except jwt.DecodeError:
        raise TokenInvalidError("Invalid refresh token")
    except jwt.ExpiredSignatureError:
        raise TokenExpiredError("Expired refresh token")

    if data.get("token_type") != "refresh":
        raise TokenInvalidError("Invalid refresh token")

    user_id = data.get("user_id")
    user_obj = DogUserModel.objects.filter(id=user_id).first()

    if not user_obj:
        raise TokenInvalidError("Invalid refresh token")

    access_token = create_jwt(user_id=user_id, token_type=AuthTokenModel.TOKEN_TYPE_ACCESS)
    refresh_token = create_jwt(user_id=user_id, token_type=AuthTokenModel.TOKEN_TYPE_REFRESH)
    expires_in = int(timedelta(hours=4).total_seconds())

    return {"access_token": access_token, "refresh_token": refresh_token, "expires_in": expires_in}
