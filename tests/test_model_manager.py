import pytest
import numpy as np
from app.ml.model_manager import ModelManager, FootballModel

def test_model_manager_init():
    """Test model manager initializes correctly"""
    manager = ModelManager()
    assert manager.model_path is not None
    assert manager.current_model is None

def test_get_current_model():
    """Test getting current model creates default if none exists"""
    manager = ModelManager()
    model = manager.get_current_model()
    
    assert model is not None
    assert isinstance(model, FootballModel)
    assert model.model is not None
    assert model.version is not None

def test_football_model_prediction():
    """Test football model can make predictions"""
    model = FootballModel("xgboost")
    
    # Create mock training data
    X = np.random.random((100, 10))
    y = np.random.randint(0, 4, 100)
    
    # Train model
    model.train(X, y)
    
    # Make prediction
    test_X = np.random.random((1, 10))
    prediction = model.predict(test_X)
    
    assert prediction is not None
    assert len(prediction) == 1

def test_model_performance_tracking():
    """Test model performance metrics are tracked"""
    manager = ModelManager()
    # Ensure model is loaded first
    model = manager.get_current_model()
    performance = manager.get_model_performance()
    
    assert isinstance(performance, dict)
    # Should have at least version info
    assert "version" in performance