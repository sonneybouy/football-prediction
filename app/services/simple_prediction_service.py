from datetime import datetime
from typing import Dict
from ..schemas.prediction import PredictionResponse

class SimplePredictionService:
    """Simplified prediction service that works without ML dependencies"""
    
    async def predict_match(
        self, 
        home_team: str, 
        away_team: str, 
        match_date: datetime
    ) -> PredictionResponse:
        
        # Simple rule-based prediction for testing
        team_strengths = {
            "Arsenal": 85,
            "Chelsea": 82,
            "Liverpool": 88,
            "Manchester City": 90,
            "Manchester United": 78,
            "Tottenham": 75
        }
        
        home_strength = team_strengths.get(home_team, 70)
        away_strength = team_strengths.get(away_team, 70)
        
        # Home advantage
        home_score = max(0, (home_strength + 10 - away_strength) / 30)
        away_score = max(0, (away_strength - home_strength) / 30)
        
        # Calculate probabilities
        if home_score > away_score:
            home_win_prob = 0.6
            away_win_prob = 0.2
            draw_prob = 0.2
        elif away_score > home_score:
            home_win_prob = 0.2
            away_win_prob = 0.6
            draw_prob = 0.2
        else:
            home_win_prob = 0.3
            away_win_prob = 0.3
            draw_prob = 0.4
        
        return PredictionResponse(
            home_team=home_team,
            away_team=away_team,
            predicted_score_home=round(home_score, 1),
            predicted_score_away=round(away_score, 1),
            win_probability_home=home_win_prob,
            win_probability_away=away_win_prob,
            draw_probability=draw_prob,
            confidence=0.75,
            model_version="1.0.0-simple",
            prediction_timestamp=datetime.utcnow()
        )