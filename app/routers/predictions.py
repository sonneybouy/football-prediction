from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..schemas.prediction import PredictionRequest, PredictionResponse
from ..services.prediction_service import PredictionService

router = APIRouter(tags=["predictions"])

@router.post("/predict", response_model=PredictionResponse)
async def predict_match(
    request: PredictionRequest,
    prediction_service: PredictionService = Depends()
):
    try:
        prediction = await prediction_service.predict_match(
            home_team=request.home_team,
            away_team=request.away_team,
            match_date=request.match_date
        )
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/predictions/recent")
async def get_recent_predictions(limit: int = 10):
    return {"message": "Recent predictions endpoint"}

@router.get("/model/performance")
async def get_model_performance():
    return {"message": "Model performance metrics"}