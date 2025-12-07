from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import authenticate
from ninja import Router

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
    user = authenticate(username=credentials.username, password=credentials.password)

    if not user:
        return (401, {"error": "Invalid credentials"})

    AuthTokenModel.objects.filter(user=user).delete()
    access_token = AuthTokenModel.objects.create(user=user, token_type=AuthTokenModel.TOKEN_TYPE_ACCESS)
    refresh_token = AuthTokenModel.objects.create(user=user, token_type=AuthTokenModel.TOKEN_TYPE_REFRESH)
    expires_in = int((access_token.expires - timezone.now()).total_seconds())

    return (200, {"access_token": access_token.key, "refresh_token": refresh_token.key, "expires_in": expires_in})
