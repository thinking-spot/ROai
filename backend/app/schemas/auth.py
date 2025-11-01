"""
Authentication schemas
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.models.user import UserRole


class UserCreate(BaseModel):
    """Schema for user registration"""
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None
    organization_name: str  # For creating new organization


class UserResponse(BaseModel):
    """Schema for user response"""
    id: int
    email: str
    full_name: Optional[str]
    role: UserRole
    organization_id: int
    is_active: bool
    is_verified: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """Schema for token payload"""
    user_id: int
    organization_id: int
    role: UserRole
