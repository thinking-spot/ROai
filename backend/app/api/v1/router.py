"""
Main API v1 router
"""
from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    organizations,
    users,
    integrations,
    ai_tools,
    metrics,
    analytics,
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(organizations.router, prefix="/organizations", tags=["organizations"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(integrations.router, prefix="/integrations", tags=["integrations"])
api_router.include_router(ai_tools.router, prefix="/ai-tools", tags=["ai-tools"])
api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
