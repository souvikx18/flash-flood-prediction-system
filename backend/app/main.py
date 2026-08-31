from fastapi import FastAPI

from app.api.auth.routes import router as auth_router
from app.api.prediction.routes import router as prediction_router


app = FastAPI(
    title="Flash Flood Prediction System API",
    version="1.0.0",
)


app.include_router(
    auth_router,
    prefix="/api",
)

app.include_router(
    prediction_router,
    prefix="/api",
)


@app.get("/")
def root():
    return {
        "message": "Flash Flood Prediction System API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }