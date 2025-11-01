"""
Integration models for external service connections
"""
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, JSON, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship
import enum
from app.models.base import BaseModel


class IntegrationType(str, enum.Enum):
    """Types of integrations"""
    # Productivity Tools
    GOOGLE_WORKSPACE = "google_workspace"
    MICROSOFT_365 = "microsoft_365"

    # Project Management
    JIRA = "jira"
    ASANA = "asana"
    MONDAY = "monday"
    LINEAR = "linear"

    # Development
    GITHUB = "github"
    GITLAB = "gitlab"
    BITBUCKET = "bitbucket"

    # CRM & Support
    SALESFORCE = "salesforce"
    HUBSPOT = "hubspot"
    ZENDESK = "zendesk"
    INTERCOM = "intercom"

    # AI Platforms
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GITHUB_COPILOT = "github_copilot"
    CURSOR = "cursor"
    GRAMMARLY = "grammarly"
    JASPER = "jasper"

    # Communication
    SLACK = "slack"
    TEAMS = "teams"


class IntegrationStatus(str, enum.Enum):
    """Integration connection status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    PENDING = "pending"


class Integration(BaseModel):
    """
    External service integration configuration
    """

    __tablename__ = "integrations"

    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    integration_type = Column(SQLEnum(IntegrationType), nullable=False)
    status = Column(SQLEnum(IntegrationStatus), default=IntegrationStatus.PENDING)

    # Configuration
    name = Column(String(255), nullable=False)  # User-friendly name
    description = Column(Text, nullable=True)
    config = Column(JSON, default=dict)  # Integration-specific configuration

    # Sync Info
    last_sync_at = Column(String(50), nullable=True)  # ISO timestamp
    sync_frequency_hours = Column(Integer, default=24)
    is_auto_sync = Column(Boolean, default=True)

    # Error tracking
    last_error = Column(Text, nullable=True)
    error_count = Column(Integer, default=0)

    # Relationships
    organization = relationship("Organization", back_populates="integrations")
    credentials = relationship("IntegrationCredential", back_populates="integration", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Integration(id={self.id}, type={self.integration_type}, status={self.status})>"


class IntegrationCredential(BaseModel):
    """
    Encrypted credentials for integrations
    """

    __tablename__ = "integration_credentials"

    integration_id = Column(Integer, ForeignKey("integrations.id"), nullable=False)

    # OAuth tokens
    access_token = Column(Text, nullable=True)  # Should be encrypted
    refresh_token = Column(Text, nullable=True)  # Should be encrypted
    token_expires_at = Column(String(50), nullable=True)  # ISO timestamp

    # API Keys
    api_key = Column(Text, nullable=True)  # Should be encrypted
    api_secret = Column(Text, nullable=True)  # Should be encrypted

    # Additional auth data
    auth_data = Column(JSON, default=dict)  # For any additional auth info

    # Relationships
    integration = relationship("Integration", back_populates="credentials")

    def __repr__(self):
        return f"<IntegrationCredential(id={self.id}, integration_id={self.integration_id})>"
