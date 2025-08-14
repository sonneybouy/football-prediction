from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Dict

class PredictionRequest(BaseModel):
    home_team: str
    away_team: str
    match_date: datetime
    league: Optional[str] = None

class PredictionResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    home_team: str
    away_team: str
    predicted_score_home: float
    predicted_score_away: float
    win_probability_home: float
    win_probability_away: float
    draw_probability: float
    confidence: float
    model_version: str
    prediction_timestamp: datetime

class MatchResult(BaseModel):
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    match_date: datetime
    league: str