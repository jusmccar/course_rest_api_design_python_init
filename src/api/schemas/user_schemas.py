from ninja import ModelSchema
from pydantic import field_validator

from core.models import DogUserModel

class DogUserCreateSchemaIn(ModelSchema):
    """Schema for dog user requests"""
    username: str

    class Meta:
        model = DogUserModel
        fields = ["username"]

    @field_validator('username')
    @classmethod
    def validate_username_length(cls, v: str) -> str:
        """Ensure username is at least 3 characters long"""
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters long")

        return v

class DogUserUpdateSchemaIn(ModelSchema):
    """Schema for dog user updates"""
    username: str | None = None
    favorite_toy: str | None = None

    class Meta:
        model = DogUserModel
        fields = ["username", "favorite_toy"]
        fields_optional = ["username", "favorite_toy"]


class DogUserSchemaOut(ModelSchema):
    """Schema for dog user responses"""

    class Meta:
        model = DogUserModel
        fields = ["id", "username", "favorite_toy"]
