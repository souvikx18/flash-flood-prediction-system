from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

    rainfall: float = Field(..., ge=0)
    temperature: float
    humidity: float = Field(..., ge=0, le=100)

    forecast_hours: int = Field(
        default=24,
        ge=1,
        le=72,
    )


class PredictionResponse(BaseModel):
    flood_probability: float = Field(
        ...,
        ge=0,
        le=1,
    )

    risk_level: str

    forecast_hours: int

    latitude: float

    longitude: float