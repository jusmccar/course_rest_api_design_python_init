from ninja import File
from ninja import ModelSchema
from ninja import Schema
from ninja.files import UploadedFile
from pydantic import field_validator

from core.models import DogUserModel


class ProfileImageUploadSchemaIn(Schema):
    """Schema for profile image upload"""
    image: UploadedFile = File(...)


class DogUserCreateSchemaIn(ModelSchema):
    """Schema for dog user requests"""
    username: str
    password: str

    class Meta:
        model = DogUserModel
        fields = ["username", "password"]

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
    profile_image_url: str | None = None

    class Meta:
        model = DogUserModel
        fields = ["id", "username", "favorite_toy"]

    @staticmethod
    def resolve_profile_image_url(obj):
        """Resolve the profile image URL"""
        if not obj.profile_image or not hasattr(obj.profile_image, "url"):
            return None

        return obj.profile_image.url


class DogUserWithTokenSchemaOut(Schema):
    """Schema for dog user with token response"""
    user: DogUserSchemaOut
    token: str
