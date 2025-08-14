import pytest
import numpy as np
from datetime import datetime
from app.services.prediction_service import PredictionService

@pytest.mark.asyncio
async def test_prediction_service_init():
    """Test prediction service initializes correctly"""
    service = PredictionService()
    assert service.model_manager is not None
    assert service.team_stats is not None

@pytest.mark.asyncio
async def test_predict_match():
    """Test prediction service can make predictions"""
    service = PredictionService()
    
    prediction = await service.predict_match(
        home_team="Arsenal",
        away_team="Chelsea", 
        match_date=datetime(2024, 12, 1, 15, 0)
    )
    
    # Check prediction structure
    assert prediction.home_team == "Arsenal"
    assert prediction.away_team == "Chelsea"
    assert isinstance(prediction.predicted_score_home, float)
    assert isinstance(prediction.predicted_score_away, float)
    assert 0 <= prediction.confidence <= 1
    assert 0 <= prediction.win_probability_home <= 1
    assert 0 <= prediction.win_probability_away <= 1
    assert 0 <= prediction.draw_probability <= 1
    
    # Probabilities should sum to approximately 1
    total_prob = (prediction.win_probability_home + 
                  prediction.win_probability_away + 
                  prediction.draw_probability)
    assert abs(total_prob - 1.0) < 0.01

def test_process_prediction():
    """Test prediction processing logic"""
    service = PredictionService()
    
    # Test with scalar prediction
    scalar_pred = np.array(2.5)
    home_score, away_score, probs = service._process_prediction(scalar_pred)
    
    assert isinstance(home_score, float)
    assert isinstance(away_score, float)
    assert home_score >= 0
    assert away_score >= 0
    assert 'home_win' in probs
    assert 'away_win' in probs
    assert 'draw' in probs
    assert 'confidence' in probs