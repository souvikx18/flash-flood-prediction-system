from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.auth import get_current_user_id
from app.database.dependencies import get_db
from app.ml.model_loader import model
from app.models.prediction import Prediction
from app.schemas.prediction import (
    PredictionHistoryResponse,
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
    db: Session = Depends(get_db),
):
    data = [[
        request.rainfall_mm_hr,
        request.elevation_m,
        request.slope_degree,
        request.rain_1h,
        request.rain_3h,
        request.rain_6h,
        request.rain_12h,
        request.rain_24h,
        request.rainfall_change,
    ]]

    prediction = int(model.predict(data)[0])

    probability = float(
        model.predict_proba(data)[0][1]
    )

    if probability >= 0.70:
        risk_level = "HIGH"
    elif probability >= 0.40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    prediction_record = Prediction(
        user_id=current_user_id,
        rainfall_mm_hr=request.rainfall_mm_hr,
        elevation_m=request.elevation_m,
        slope_degree=request.slope_degree,
        rain_1h=request.rain_1h,
        rain_3h=request.rain_3h,
        rain_6h=request.rain_6h,
        rain_12h=request.rain_12h,
        rain_24h=request.rain_24h,
        rainfall_change=request.rainfall_change,
        prediction=prediction,
        flood_probability=probability,
        risk_level=risk_level,
    )

    db.add(prediction_record)
    db.commit()

    return PredictionResponse(
        prediction=prediction,
        flood_probability=probability,
        risk_level=risk_level,
    )

@router.get(
    "/history",
    response_model=list[PredictionHistoryResponse],
)
def prediction_history(
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=50,
        ge=1,
        le=100,
    ),
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    predictions = (
    db.query(Prediction)
        .filter(Prediction.user_id == current_user_id)
        .order_by(Prediction.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return predictions