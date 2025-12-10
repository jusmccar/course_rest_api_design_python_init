from django.contrib.auth import authenticate
from django.utils import timezone

from api.logic.exceptions import AuthenticationError
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
