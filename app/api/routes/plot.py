from fastapi import APIRouter, HTTPException
from app.db.postgres import load_training_data
from app.storage.redis_storage import latest_model
from app.utils.plotting import plot_timeseries

router = APIRouter()

@router.get("/plot", tags=["Plot"])
def plot(series_id: str, version: str):
    ts = load_training_data(series_id, version)
    if not ts.data:
        raise HTTPException(status_code=404, detail="No training data")
    
    model, _ = latest_model(series_id)
    return plot_timeseries(ts, model, series_id, version)
