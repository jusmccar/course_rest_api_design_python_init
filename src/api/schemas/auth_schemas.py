from ninja import Schema

class TokenRequestSchemaIn(Schema):
    """Schema for token requests with username and password"""
    username: str
    password: str

class TokenRequestSchemaOut(Schema):
    """Schema for token responses"""
    access_token: str
    refresh_token: str
    expires_in: int

class RefreshTokenRequestSchemaIn(Schema):
    """Schema for refresh token requests"""
    refresh_token: str
