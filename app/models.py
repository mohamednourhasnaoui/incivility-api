from sqlmodel import SQLModel

class Report(SQLModel):
    id: int
    description: str
