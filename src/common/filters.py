from ninja import Field
from ninja import FilterSchema


class UsersFilter(FilterSchema):
    """
    Filter schema for user endpoints.
    """
    username: str | None = Field(None, q="username__icontains")
    favorite_toy: str | None = Field(None, q="favorite_toy__icontains")
