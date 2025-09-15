from fastapi import APIRouter
from .routes import training, prediction, health, plot, metrics

api_router = APIRouter()
api_router.include_router(training.router)
api_router.include_router(prediction.router)
api_router.include_router(health.router)
api_router.include_router(plot.router)
api_router.include_router(metrics.router)