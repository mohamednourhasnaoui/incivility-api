from pydantic import BaseModel

class ReportCreate(BaseModel):
    id: int
    description: str
