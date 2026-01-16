from fastapi import FastAPI
from app.routers import reports

app = FastAPI(
    title="Tunis Incivility API",
    description="Report and track public incivility in Tunis",
    version="1.0.0"
)

# Include your routers
app.include_router(reports.router, prefix="/api/v1/reports", tags=["Reports"])

@app.get("/")
async def root():
    return {"message": "Incivility API is live!"}
