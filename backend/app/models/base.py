"""
Base model with common fields for all database models
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.sql import func
from app.core.database import Base


class BaseModel(Base):
    """
    Abstract base model with common fields
    """

    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def dict(self):
        """
        Convert model to dictionary
        """
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
