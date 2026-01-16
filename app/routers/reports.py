from fastapi import APIRouter

router = APIRouter()

# Sample GET endpoint
@router.get("/")
async def get_reports():
    return {"reports": [{"id": 1, "description": "Someone shouting at market"}]}

# Sample POST endpoint
@router.post("/")
async def create_report(description: str):
    return {"message": "Report received", "description": description}
