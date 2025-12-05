from ninja import Schema

class TokenRequestSchemaIn(Schema):
    """Schema for token requests"""
    username: str
    password: str

class TokenRequestSchemaOut(Schema):
    """Schema for token responses"""
    token: str
