from ninja import ModelSchema
from ninja import Schema
from pydantic import field_validator

from api.schemas.user_schemas import DogUserSchemaOut
from core.models import BarkModel

class BarkCreateSchemaIn(ModelSchema):
    """Schema for bark creations"""
    message: str

    class Meta:
        model = BarkModel
        fields = ["message"]

    @field_validator('message')
    @classmethod
    def validate_message_not_empty(cls, v: str) -> str:
        """Ensure message isn't just whitespace"""
        if not v.strip():
            raise ValueError("Message cannot be empty or just whitespace")

        return v

class BarkSchemaIn(Schema):
    """Schema for bark requests"""
    message: str

class BarkSchemaOut(ModelSchema):
    """Schema for bark responses"""
    user: DogUserSchemaOut
    created_time: str
    created_date: str

    class Meta:
        model = BarkModel
        fields = ["id", "message"]

    @staticmethod
    def resolve_created_time(obj):
        """Resolve created_time in HH:MM AM/PM format from created_at field"""
        return obj.created_at.strftime("%I:%M %p")

    @staticmethod
    def resolve_created_date(obj):
        """Resolve created_date in DDMonYY format from created_at field"""
        return obj.created_at.strftime("%d%b%y")


class ErrorSchemaOut(Schema):
    """Schema for error responses"""
    error : str
