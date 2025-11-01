"""
User model
"""
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum
from app.models.base import BaseModel


class UserRole(str, enum.Enum):
    """User roles for access control"""
    SUPER_ADMIN = "super_admin"  # Platform admin
    ORG_ADMIN = "org_admin"  # Organization administrator
    ANALYST = "analyst"  # Can view all analytics
    MANAGER = "manager"  # Can view team analytics
    MEMBER = "member"  # Basic user


class User(BaseModel):
    """
    User model with role-based access control
    """

    __tablename__ = "users"

    # Basic Info
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    # Role & Organization
    role = Column(SQLEnum(UserRole), default=UserRole.MEMBER, nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)

    # Profile
    avatar_url = Column(String(500), nullable=True)
    timezone = Column(String(50), default="UTC")
    job_title = Column(String(100), nullable=True)
    department = Column(String(100), nullable=True)

    # Relationships
    organization = relationship("Organization", back_populates="users")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"

    @property
    def is_admin(self) -> bool:
        """Check if user has admin privileges"""
        return self.role in [UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN]

    @property
    def can_view_all_analytics(self) -> bool:
        """Check if user can view all organization analytics"""
        return self.role in [UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN, UserRole.ANALYST]
