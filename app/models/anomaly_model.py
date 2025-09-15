import numpy as np
from app.models.pydantic_models import TimeSeries, DataPoint

class AnomalyDetectionModel:
    def __init__(self):
        self.mean = None
        self.std = None

    def fit(self, data: TimeSeries):
        values = [d.value for d in data.data]
        self.mean = np.mean(values)
        self.std = np.std(values)

    def predict(self, point: DataPoint) -> bool:
        if self.mean is None or self.std is None:
            raise ValueError("Model not trained")
        return point.value > self.mean + 3 * self.std
