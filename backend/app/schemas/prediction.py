from datetime import datetime
from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    rainfall_mm_hr: float = Field(..., ge=0)
    elevation_m: float
    slope_degree: float = Field(..., ge=0)
    rain_1h: float = Field(..., ge=0)
    rain_3h: float = Field(..., ge=0)
    rain_6h: float = Field(..., ge=0)
    rain_12h: float = Field(..., ge=0)
    rain_24h: float = Field(..., ge=0)
    rainfall_change: float


class PredictionResponse(BaseModel):
    prediction: int
    flood_probability: float = Field(..., ge=0, le=1)
    risk_level: str


class PredictionHistoryResponse(BaseModel):
    id: int
    user_id: int

    rainfall_mm_hr: float
    elevation_m: float
    slope_degree: float
    rain_1h: float
    rain_3h: float
    rain_6h: float
    rain_12h: float
    rain_24h: float
    rainfall_change: float

    prediction: int
    flood_probability: float
    risk_level: str
    created_at: datetime

    model_config = {"from_attributes": True}