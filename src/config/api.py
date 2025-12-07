from ninja import NinjaAPI

from api.endpoints.auth import router as auth_router
from api.endpoints.barks import router as barks_router
from api.endpoints.users import router as users_router
from common.auth.jwt_auth import JWTAuth
from common.auth.token import TokenAuth

api = NinjaAPI(auth=[TokenAuth(), JWTAuth()], title="Social Dog API")

api.add_router("/auth", auth_router, tags=["auth"])
api.add_router("/users", users_router, tags=["users"])
api.add_router("/barks", barks_router, tags=["barks"])
