"""
Organization schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class OrganizationCreate(BaseModel):
    """Schema for creating an organization"""
    name: str = Field(..., min_length=2, max_length=255)
    slug: str = Field(..., min_length=2, max_length=100)
    domain: Optional[str] = None
    employee_count: Optional[int] = None
    primary_contact_email: Optional[str] = None
    primary_contact_name: Optional[str] = None


class OrganizationUpdate(BaseModel):
    """Schema for updating an organization"""
    name: Optional[str] = None
    domain: Optional[str] = None
    employee_count: Optional[int] = None
    subscription_tier: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None


class OrganizationResponse(BaseModel):
    """Schema for organization response"""
    id: int
    name: str
    slug: str
    domain: Optional[str]
    subscription_tier: str
    is_active: bool
    employee_count: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
