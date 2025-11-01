"""
Metrics management endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

router = APIRouter()


@router.post("/")
async def create_metric(
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new metric to track
    """
    # TODO: Implement metric creation
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/")
async def list_metrics(
    db: AsyncSession = Depends(get_db)
):
    """
    List all metrics being tracked
    """
    # TODO: Implement metrics listing
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{metric_id}/snapshots")
async def get_metric_snapshots(
    metric_id: int,
    start_date: str = None,
    end_date: str = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Get time-series snapshots for a metric
    """
    # TODO: Implement snapshot retrieval
    raise HTTPException(status_code=501, detail="Not implemented")
