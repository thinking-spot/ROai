"""
Organization model for multi-tenant architecture
"""
from sqlalchemy import Column, String, Boolean, Integer, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Organization(BaseModel):
    """
    Organization/Company - the tenant in multi-tenant architecture
    """

    __tablename__ = "organizations"

    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    domain = Column(String(255), nullable=True)  # Company domain for email verification

    # Subscription & Billing
    subscription_tier = Column(String(50), default="trial")  # trial, starter, professional, enterprise
    is_active = Column(Boolean, default=True)
    employee_count = Column(Integer, nullable=True)

    # Settings
    settings = Column(JSON, default=dict)  # Flexible settings storage

    # Contact Info
    primary_contact_email = Column(String(255), nullable=True)
    primary_contact_name = Column(String(255), nullable=True)

    # Relationships
    users = relationship("User", back_populates="organization", cascade="all, delete-orphan")
    integrations = relationship("Integration", back_populates="organization", cascade="all, delete-orphan")
    ai_tools = relationship("AITool", back_populates="organization", cascade="all, delete-orphan")
    metrics = relationship("Metric", back_populates="organization", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Organization(id={self.id}, name={self.name}, slug={self.slug})>"
