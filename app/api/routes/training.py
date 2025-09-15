from fastapi import APIRouter
import time
import mlflow
from app.models.pydantic_models import TrainData, TrainResponse, TimeSeries, DataPoint
from app.models.anomaly_model import AnomalyDetectionModel
from app.storage.redis_storage import save_model
from app.db.postgres import save_training_data
from app.core.metrics import train_requests, train_duration
import os

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

router = APIRouter()

@router.post("/fit/{series_id}", response_model=TrainResponse, tags=["Training"])
def fit(series_id: str, data: TrainData):
    train_requests.inc()
    start = time.time()

    ts = TimeSeries(data=[DataPoint(timestamp=ts, value=val) for ts, val in zip(data.timestamps, data.values)])
    
    model = AnomalyDetectionModel()
    model.fit(ts)

    version = save_model(series_id, model)
    save_training_data(series_id, version, ts)

    duration = time.time() - start
    train_duration.observe(duration)

    with mlflow.start_run(run_name=f"train_{series_id}_{version}"):
        mlflow.log_param("series_id", series_id)
        mlflow.log_param("version", version)
        mlflow.log_metric("train_duration", duration)
        mlflow.log_metric("mean", model.mean)
        mlflow.log_metric("std", model.std)
        mlflow.sklearn.log_model(model, artifact_path="model")

    return {"series_id": series_id, "version": version, "points_used": len(ts.data)}
