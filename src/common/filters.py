from typing import Optional
from ninja import Schema


class UsersFilter(Schema):
    """
    Filter schema for user endpoints.
    """
    username: str | None = None
    favorite_toy: str | None = None
