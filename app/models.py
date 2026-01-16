from sqlmodel import SQLModel, Field
from geoalchemy2 import Geometry
from typing import Optional
from datetime import datetime

class Report(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str
    location: str  # WKT Point string (e.g., "POINT(10.181 36.806)")
    occurred_at: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
