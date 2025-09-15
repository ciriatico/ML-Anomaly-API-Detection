from fastapi import APIRouter
from app.core.metrics import train_duration, predict_duration
from app.db.postgres import count_trained_series

router = APIRouter()

def to_ms(hist):
    total, count = 0, 0
    for s in hist.collect()[0].samples:
        if s.name.endswith("_sum"):
            total = s.value
        elif s.name.endswith("_count"):
            count = s.value
    avg = (total / count) * 1000 if count > 0 else 0
    return {"avg": avg, "p95": avg}

@router.get("/healthcheck", tags=["Health Check"])
def healthcheck():
    return {
        "series_trained": count_trained_series(),
        "inference_latency_ms": to_ms(predict_duration),
        "training_latency_ms": to_ms(train_duration),
    }
