from typing import List
from pydantic import BaseModel, Field

class DataPoint(BaseModel):
    timestamp: int
    value: float

class TimeSeries(BaseModel):
    data: List[DataPoint]

class TrainData(BaseModel):
    timestamps: List[int] = Field(..., description="Unix timestamps")
    values: List[float] = Field(..., description="Values at timestamps")

class TrainResponse(BaseModel):
    series_id: str
    version: str
    points_used: int

class PredictData(BaseModel):
    timestamp: str
    value: float

class PredictResponse(BaseModel):
    anomaly: bool
    model_version: str
