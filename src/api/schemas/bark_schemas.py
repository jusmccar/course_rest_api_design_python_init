from ninja import ModelSchema
from ninja import Schema

from api.schemas.user_schemas import DogUserSchemaOut
from core.models import BarkModel

class BarkSchemaIn(Schema):
    """Schema for bark requests"""
    message: str

class BarkSchemaOut(ModelSchema):
    """Schema for bark responses"""

    user: DogUserSchemaOut

    class Meta:
        model = BarkModel
        fields = ['id', 'message']

class ErrorSchemaOut(Schema):
    """Schema for error responses"""
    error : str
