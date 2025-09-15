import joblib
import io
import redis
from app.models.anomaly_model import AnomalyDetectionModel
from app.core.config import REDIS_HOST, REDIS_PORT

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

def save_model(series_id: str, model: AnomalyDetectionModel) -> str:
    version_num = r.incr(f"model:{series_id}:version_counter")
    version = f"v{version_num}"
    key = f"model:{series_id}:{version}"

    buffer = io.BytesIO()
    joblib.dump(model, buffer)
    buffer.seek(0)

    r.set(key, buffer.read())
    r.set(f"model:{series_id}:latest", version)
    r.rpush(f"model:{series_id}:versions", version)
    return version

def load_model(series_id: str, version: str):
    key = f"model:{series_id}:{version}"
    data = r.get(key)
    if not data:
        return None
    buffer = io.BytesIO(data)
    return joblib.load(buffer)

def latest_model(series_id: str):
    version = r.get(f"model:{series_id}:latest")
    if not version:
        return None, None
    version = version.decode("utf-8")
    return load_model(series_id, version), version

def list_versions(series_id: str):
    versions = r.lrange(f"model:{series_id}:versions", 0, -1)
    return [v.decode("utf-8") for v in versions]
