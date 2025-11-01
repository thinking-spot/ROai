"""
AI Tool tracking models
"""
from sqlalchemy import Column, String, Integer, ForeignKey, JSON, Enum as SQLEnum, Float, Text
from sqlalchemy.orm import relationship
import enum
from app.models.base import BaseModel


class AIToolCategory(str, enum.Enum):
    """Categories of AI tools"""
    CODE_ASSISTANT = "code_assistant"  # GitHub Copilot, Cursor, etc.
    WRITING_ASSISTANT = "writing_assistant"  # Grammarly, Jasper, etc.
    CHAT_ASSISTANT = "chat_assistant"  # ChatGPT, Claude, etc.
    CUSTOMER_SUPPORT = "customer_support"  # AI chatbots, support agents
    DATA_ANALYSIS = "data_analysis"  # AI analytics tools
    DESIGN = "design"  # Midjourney, DALL-E, etc.
    SALES_MARKETING = "sales_marketing"  # AI sales/marketing tools
    HR_RECRUITING = "hr_recruiting"  # AI recruiting tools
    OTHER = "other"


class AITool(BaseModel):
    """
    AI Tool configuration and tracking
    """

    __tablename__ = "ai_tools"

    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    integration_id = Column(Integer, ForeignKey("integrations.id"), nullable=True)

    # Tool Info
    name = Column(String(255), nullable=False)
    vendor = Column(String(255), nullable=True)
    category = Column(SQLEnum(AIToolCategory), nullable=False)
    description = Column(Text, nullable=True)

    # Deployment Info
    deployment_date = Column(String(50), nullable=True)  # ISO timestamp
    is_active = Column(Boolean, default=True)

    # Pricing
    cost_model = Column(String(50), nullable=True)  # per_user, per_token, per_request, fixed
    monthly_cost = Column(Float, nullable=True)
    cost_per_unit = Column(Float, nullable=True)  # Cost per token/request if applicable

    # License Info
    total_licenses = Column(Integer, nullable=True)
    active_users = Column(Integer, default=0)

    # Target Metrics (what we expect to improve)
    target_metrics = Column(JSON, default=list)  # List of metric names we're tracking
    expected_roi = Column(Float, nullable=True)  # Expected ROI percentage

    # Relationships
    organization = relationship("Organization", back_populates="ai_tools")
    integration = relationship("Integration")
    usage_records = relationship("AIToolUsage", back_populates="ai_tool", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<AITool(id={self.id}, name={self.name}, category={self.category})>"


class AIToolUsage(BaseModel):
    """
    Time-series usage data for AI tools
    """

    __tablename__ = "ai_tool_usage"

    ai_tool_id = Column(Integer, ForeignKey("ai_tools.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Null for aggregate data

    # Time period
    period_start = Column(String(50), nullable=False)  # ISO timestamp
    period_end = Column(String(50), nullable=False)  # ISO timestamp
    granularity = Column(String(20), default="daily")  # hourly, daily, weekly, monthly

    # Usage Metrics
    total_requests = Column(Integer, default=0)
    total_tokens = Column(Integer, nullable=True)  # For token-based APIs
    total_cost = Column(Float, nullable=True)
    active_time_minutes = Column(Integer, nullable=True)  # Time spent using the tool

    # Feature Usage (JSON for flexibility)
    feature_usage = Column(JSON, default=dict)  # Which features were used and how often

    # Quality Metrics (if available)
    error_count = Column(Integer, default=0)
    success_rate = Column(Float, nullable=True)  # Percentage

    # Relationships
    ai_tool = relationship("AITool", back_populates="usage_records")
    user = relationship("User")

    def __repr__(self):
        return f"<AIToolUsage(id={self.id}, ai_tool_id={self.ai_tool_id}, period={self.granularity})>"
