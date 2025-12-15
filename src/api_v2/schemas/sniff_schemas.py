from uuid import UUID

from ninja import Schema

from api_v2.schemas.bark_schemas import BarkSchemaOut


class SniffCreateSchemaIn(Schema):
    """Schema for creating sniffs"""

    bark_id: UUID


class SniffSchemaOut(BarkSchemaOut):
    """Schema for sniff responses"""

    pass
