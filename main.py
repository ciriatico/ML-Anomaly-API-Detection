from fastapi import FastAPI
from app.api import router
from prometheus_client import make_asgi_app

app = FastAPI(title="Anomaly Detection API")

# API routes
app.include_router(router)

# Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
