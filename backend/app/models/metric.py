"""
Productivity metrics models
"""
from sqlalchemy import Column, String, Integer, ForeignKey, JSON, Enum as SQLEnum, Float, Boolean
from sqlalchemy.orm import relationship
import enum
from app.models.base import BaseModel


class MetricType(str, enum.Enum):
    """Types of productivity metrics"""
    # Communication Metrics
    EMAIL_RESPONSE_TIME = "email_response_time"
    EMAIL_VOLUME = "email_volume"
    MEETING_TIME = "meeting_time"

    # Document Metrics
    DOCUMENTS_CREATED = "documents_created"
    DOCUMENTS_EDITED = "documents_edited"
    DOCUMENT_COLLABORATION = "document_collaboration"

    # Development Metrics
    CODE_COMMITS = "code_commits"
    PULL_REQUESTS = "pull_requests"
    CODE_REVIEW_TIME = "code_review_time"
    BUILD_SUCCESS_RATE = "build_success_rate"
    BUGS_FIXED = "bugs_fixed"
    LINES_OF_CODE = "lines_of_code"

    # Project Management Metrics
    TASKS_COMPLETED = "tasks_completed"
    TASK_CYCLE_TIME = "task_cycle_time"
    SPRINT_VELOCITY = "sprint_velocity"
    STORY_POINTS = "story_points"

    # Support Metrics
    TICKETS_RESOLVED = "tickets_resolved"
    FIRST_RESPONSE_TIME = "first_response_time"
    RESOLUTION_TIME = "resolution_time"
    CUSTOMER_SATISFACTION = "customer_satisfaction"

    # Sales Metrics
    DEALS_CLOSED = "deals_closed"
    SALES_CYCLE_LENGTH = "sales_cycle_length"
    PIPELINE_VALUE = "pipeline_value"
    CONVERSION_RATE = "conversion_rate"

    # Custom Metrics
    CUSTOM = "custom"


class MetricSource(str, enum.Enum):
    """Source system for the metric"""
    GOOGLE_WORKSPACE = "google_workspace"
    MICROSOFT_365 = "microsoft_365"
    JIRA = "jira"
    GITHUB = "github"
    SALESFORCE = "salesforce"
    ZENDESK = "zendesk"
    MANUAL = "manual"
    CALCULATED = "calculated"


class Metric(BaseModel):
    """
    Metric definition and configuration
    """

    __tablename__ = "metrics"

    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)

    # Metric Info
    name = Column(String(255), nullable=False)
    metric_type = Column(SQLEnum(MetricType), nullable=False)
    source = Column(SQLEnum(MetricSource), nullable=False)
    description = Column(String(500), nullable=True)

    # Configuration
    unit = Column(String(50), nullable=True)  # hours, count, percentage, dollars, etc.
    aggregation_method = Column(String(50), default="sum")  # sum, avg, min, max, count
    is_higher_better = Column(Boolean, default=True)  # For interpreting improvements

    # Target Values
    target_value = Column(Float, nullable=True)
    baseline_value = Column(Float, nullable=True)

    # AI Tool Association (optional - for tracking specific AI tool impact)
    tracked_ai_tool_id = Column(Integer, ForeignKey("ai_tools.id"), nullable=True)

    # Filters & Segmentation
    filters = Column(JSON, default=dict)  # For filtering data (e.g., department, team)

    # Status
    is_active = Column(Boolean, default=True)

    # Relationships
    organization = relationship("Organization", back_populates="metrics")
    tracked_ai_tool = relationship("AITool")
    snapshots = relationship("MetricSnapshot", back_populates="metric", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Metric(id={self.id}, name={self.name}, type={self.metric_type})>"


class MetricSnapshot(BaseModel):
    """
    Time-series snapshots of metric values
    """

    __tablename__ = "metric_snapshots"

    metric_id = Column(Integer, ForeignKey("metrics.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Null for aggregate data
    ai_tool_id = Column(Integer, ForeignKey("ai_tools.id"), nullable=True)  # Which AI tool influenced this

    # Time Period
    period_start = Column(String(50), nullable=False)  # ISO timestamp
    period_end = Column(String(50), nullable=False)  # ISO timestamp
    granularity = Column(String(20), default="daily")  # hourly, daily, weekly, monthly

    # Metric Value
    value = Column(Float, nullable=False)
    sample_size = Column(Integer, nullable=True)  # For statistical significance

    # Context
    context = Column(JSON, default=dict)  # Additional context data
    tags = Column(JSON, default=list)  # For categorization

    # AI Usage Flag
    with_ai = Column(Boolean, nullable=True)  # Was AI tool being used during this period?

    # Relationships
    metric = relationship("Metric", back_populates="snapshots")
    user = relationship("User")
    ai_tool = relationship("AITool")

    def __repr__(self):
        return f"<MetricSnapshot(id={self.id}, metric_id={self.metric_id}, value={self.value})>"
