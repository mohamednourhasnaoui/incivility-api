from fastapi import FastAPI
from app.routers import reports

app = FastAPI(title="Incivility API")

# Include routers
app.include_router(reports.router, prefix="/api/v1/reports", tags=["Reports"])

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Incivility API is live!"}
