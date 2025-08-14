from datetime import datetime
from typing import Dict, List
import pandas as pd
import numpy as np
from ..schemas.prediction import PredictionResponse
from ..ml.model_manager import ModelManager
from ..data.team_stats import TeamStatsService

class PredictionService:
    def __init__(self):
        self.model_manager = ModelManager()
        self.team_stats = TeamStatsService()
    
    async def predict_match(
        self, 
        home_team: str, 
        away_team: str, 
        match_date: datetime
    ) -> PredictionResponse:
        
        # Get team features
        home_features = await self.team_stats.get_team_features(home_team)
        away_features = await self.team_stats.get_team_features(away_team)
        
        # Prepare input features
        features = self._prepare_features(home_features, away_features)
        
        # Make prediction
        model = self.model_manager.get_current_model()
        prediction = model.predict(features)
        
        # Convert to probabilities and scores
        home_score, away_score, probabilities = self._process_prediction(prediction)
        
        return PredictionResponse(
            home_team=home_team,
            away_team=away_team,
            predicted_score_home=home_score,
            predicted_score_away=away_score,
            win_probability_home=probabilities['home_win'],
            win_probability_away=probabilities['away_win'],
            draw_probability=probabilities['draw'],
            confidence=probabilities['confidence'],
            model_version=model.version,
            prediction_timestamp=datetime.utcnow()
        )
    
    def _prepare_features(self, home_features: Dict, away_features: Dict) -> np.ndarray:
        # Combine and normalize features
        feature_vector = []
        
        # Home team features
        feature_vector.extend([
            home_features.get('avg_goals_scored', 0),
            home_features.get('avg_goals_conceded', 0),
            home_features.get('home_advantage', 0),
            home_features.get('recent_form', 0),
        ])
        
        # Away team features
        feature_vector.extend([
            away_features.get('avg_goals_scored', 0),
            away_features.get('avg_goals_conceded', 0),
            away_features.get('away_form', 0),
        ])
        
        # Head-to-head features
        h2h = self.team_stats.get_head_to_head(home_features['team'], away_features['team'])
        feature_vector.extend([
            h2h.get('home_wins', 0),
            h2h.get('away_wins', 0),
            h2h.get('draws', 0),
        ])
        
        return np.array(feature_vector).reshape(1, -1)
    
    def _process_prediction(self, prediction: np.ndarray) -> tuple:
        # Handle both scalar and array predictions
        if prediction.ndim == 0 or len(prediction.shape) == 1:
            # Scalar prediction - split it into home/away scores
            if prediction.ndim == 0:
                total_goals = max(0, float(prediction.item()))
            else:
                total_goals = max(0, float(prediction[0]))
            home_score = total_goals * 0.6  # Home advantage
            away_score = total_goals * 0.4
        else:
            # Array prediction with [home, away] scores
            home_score = max(0, float(prediction[0][0]))
            away_score = max(0, float(prediction[0][1]))
        
        # Calculate probabilities based on score difference
        score_diff = home_score - away_score
        
        if score_diff > 0.5:
            home_win_prob = 0.6
            away_win_prob = 0.2
            draw_prob = 0.2
        elif score_diff < -0.5:
            home_win_prob = 0.2
            away_win_prob = 0.6
            draw_prob = 0.2
        else:
            home_win_prob = 0.3
            away_win_prob = 0.3
            draw_prob = 0.4
        
        return home_score, away_score, {
            'home_win': home_win_prob,
            'away_win': away_win_prob,
            'draw': draw_prob,
            'confidence': 0.75
        }