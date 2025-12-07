from datetime import timedelta
import time
import jwt

from django.conf import settings
from ninja.security import HttpBearer

from core.models import DogUserModel

class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        except jwt.PyJWTError:
            return None

        if payload.get("token_type") != "access":
            return None

        user_id = payload.get("user_id")
        obj = DogUserModel.objects.filter(id=user_id).first()

        if not obj:
            return None

        return obj

def create_jwt(user_id, token_type):
    """
    Create a signed JWT for a user.

    Args:
        user_id: UUID of the user
        token_type: "access" or "refresh"

    Returns:
        Encoded JWT string
    """

    # Determine expiration window
    if token_type == "access":
        exp_seconds = int(timedelta(hours=4).total_seconds())
    elif token_type == "refresh":
        exp_seconds = int(timedelta(days=7).total_seconds())
    else:
        raise ValueError("Invalid token_type. Must be 'access' or 'refresh'.")

    now = int(time.time())

    payload = {
        "user_id": str(user_id),
        "token_type": token_type,
        "iat": now,
        "exp": now + exp_seconds,
    }

    # Encode with HS256 using settings.JWT_SECRET
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

    return token
