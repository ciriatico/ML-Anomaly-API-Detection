from fastapi import APIRouter, Query, HTTPException
import time
from app.models.pydantic_models import PredictData, PredictResponse, DataPoint
from app.storage.redis_storage import latest_model, load_model
from app.core.metrics import predict_requests, predict_duration

router = APIRouter()

@router.post("/predict/{series_id}", response_model=PredictResponse, tags=["Prediction"])
def predict(series_id: str, point: PredictData, version: str = Query(default=None)):
    predict_requests.inc()
    start = time.time()

    # Load model
    if version is None:
        model, model_version = latest_model(series_id)
    else:
        model = load_model(series_id, version)
        model_version = version

    if model is None:
        raise HTTPException(status_code=404, detail="No model found for series_id")

    # Parse timestamp
    try:
        timestamp = int(point.timestamp)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid timestamp format, must be int-like string")

    result = bool(model.predict(DataPoint(timestamp=timestamp, value=point.value)))
    predict_duration.observe(time.time() - start)

    return {"anomaly": result, "model_version": model_version}
