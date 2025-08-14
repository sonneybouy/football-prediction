import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root_endpoint():
    """Test the root endpoint returns HTML"""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_prediction_endpoint_validation():
    """Test prediction endpoint with invalid data"""
    response = client.post(
        "/api/v1/predict",
        json={"invalid": "data"}
    )
    # Should return validation error
    assert response.status_code == 422

def test_prediction_endpoint_valid_data():
    """Test prediction endpoint with valid data"""
    response = client.post(
        "/api/v1/predict",
        json={
            "home_team": "Arsenal",
            "away_team": "Chelsea",
            "match_date": "2024-12-01T15:00:00"
        }
    )
    # Should return prediction
    assert response.status_code == 200
    data = response.json()
    assert "predicted_score_home" in data
    assert "predicted_score_away" in data
    assert "confidence" in data