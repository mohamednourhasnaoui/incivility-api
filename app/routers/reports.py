from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db import get_session
from app.models import Report
from sqlmodel import select
from datetime import datetime

router = APIRouter()

# Create report
@router.post("/")
async def create_report(description: str, lat: float, lon: float, db: AsyncSession = Depends(get_session)):
    point_wkt = f"POINT({lon} {lat})"
    report = Report(description=description, location=point_wkt, occurred_at=datetime.utcnow())
    db.add(report)
    await db.commit()
    await db.refresh(report)
    return {"message": "Report received", "id": report.id, "description": report.description}

# Get all reports
@router.get("/")
async def get_reports(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Report))
    reports = result.scalars().all()
    return {"reports": [{"id": r.id, "description": r.description, "location": r.location} for r in reports]}
