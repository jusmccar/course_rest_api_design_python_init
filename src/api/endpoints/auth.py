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

    token, created = AuthTokenModel.objects.get_or_create(user=user)

    return (200, {"token": token.key})
