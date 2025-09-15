from fastapi import FastAPI

from app.core import metrics
from app.api.router import api_router

app = FastAPI(title="Anomaly Detection API")
app.include_router(api_router)
