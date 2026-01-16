from fastapi import APIRouter
from typing import List
from pydantic import BaseModel

router = APIRouter()

# Example schemas
class Report(BaseModel):
    id: int
    description: str

# Fake in-memory database
reports_db: List[Report] = []

@router.get("/", response_model=List[Report])
async def get_reports():
    return reports_db

@router.post("/", response_model=Report, status_code=201)
async def create_report(report: Report):
    reports_db.append(report)
    return report
