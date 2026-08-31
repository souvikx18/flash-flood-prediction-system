from fastapi import APIRouter, Depends

from app.core.auth import get_current_user_id
from app.schemas.prediction import (
    PredictionRequest,
    PredictionResponse,
)


router = APIRouter(
    prefix="/prediction",
    tags=["Prediction"],
)


@router.post(
    "/predict",
    response_model=PredictionResponse,
)
def predict(
    request: PredictionRequest,
    current_user_id: int = Depends(get_current_user_id),
):
    # Temporary response.
    # This will be replaced with ML model.
    flood_probability = 0.0

    return PredictionResponse(
        flood_probability=flood_probability,
        risk_level="LOW",
        forecast_hours=request.forecast_hours,
        latitude=request.latitude,
        longitude=request.longitude,
    )