from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import detection, drift, ais, attribution, report
from app.core.database import engine
from app.models.incident import Base

# Create tables (in production use migrations)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Maritrace API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(detection.router, prefix="/api/v1/detection", tags=["Detection"])
app.include_router(drift.router, prefix="/api/v1/drift", tags=["Drift"])
app.include_router(ais.router, prefix="/api/v1/ais", tags=["AIS"])
app.include_router(attribution.router, prefix="/api/v1/attribution", tags=["Attribution"])
app.include_router(report.router, prefix="/api/v1/report", tags=["Report"])

@app.get("/")
def root():
    return {"message": "Maritrace API is running"}