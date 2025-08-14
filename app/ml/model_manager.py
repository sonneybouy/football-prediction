import joblib
import os
import numpy as np
from datetime import datetime
from typing import Dict, Any
import xgboost as xgb
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
import pandas as pd
from ..core.config import settings

class FootballModel:
    def __init__(self, model_type: str = "xgboost"):
        self.model_type = model_type
        self.model = None
        self.version = "1.0.0"
        self.trained_at = None
        self.performance_metrics = {}
        
        if model_type == "xgboost":
            self.model = xgb.XGBRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            )
        elif model_type == "random_forest":
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
    
    def train(self, X: np.ndarray, y: np.ndarray):
        """Train the model"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        self.model.fit(X_train, y_train)
        self.trained_at = datetime.utcnow()
        
        # Calculate performance metrics
        y_pred = self.model.predict(X_test)
        self.performance_metrics = {
            'mse': mean_squared_error(y_test, y_pred),
            'mae': mean_absolute_error(y_test, y_pred),
            'train_samples': len(X_train),
            'test_samples': len(X_test)
        }
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions"""
        if self.model is None:
            raise ValueError("Model not trained yet")
        return self.model.predict(X)
    
    def save(self, filepath: str):
        """Save model to disk"""
        model_data = {
            'model': self.model,
            'model_type': self.model_type,
            'version': self.version,
            'trained_at': self.trained_at,
            'performance_metrics': self.performance_metrics
        }
        joblib.dump(model_data, filepath)
    
    @classmethod
    def load(cls, filepath: str):
        """Load model from disk"""
        model_data = joblib.load(filepath)
        instance = cls(model_data['model_type'])
        instance.model = model_data['model']
        instance.version = model_data['version']
        instance.trained_at = model_data['trained_at']
        instance.performance_metrics = model_data['performance_metrics']
        return instance

class ModelManager:
    def __init__(self):
        self.current_model = None
        self.model_path = settings.model_path
        self.ensure_model_directory()
    
    def ensure_model_directory(self):
        """Create model directory if it doesn't exist"""
        os.makedirs(self.model_path, exist_ok=True)
    
    def get_current_model(self) -> FootballModel:
        """Get the current active model"""
        if self.current_model is None:
            self.load_latest_model()
        
        if self.current_model is None:
            # Create a default model with mock training
            self.current_model = self.create_default_model()
        
        return self.current_model
    
    def create_default_model(self) -> FootballModel:
        """Create a default model with synthetic training data"""
        model = FootballModel("xgboost")
        
        # Generate synthetic training data
        np.random.seed(42)
        n_samples = 1000
        n_features = 10
        
        # Mock features: team stats, form, etc.
        X = np.random.random((n_samples, n_features))
        
        # Mock target: [home_score, away_score]
        y = np.column_stack([
            np.random.poisson(1.5, n_samples),  # home scores
            np.random.poisson(1.2, n_samples)   # away scores
        ])
        
        # Simple model that predicts sum of goals
        y_simple = np.sum(y, axis=1)
        model.model.fit(X, y_simple)
        model.trained_at = datetime.utcnow()
        model.version = "1.0.0-default"
        
        return model
    
    def train_new_model(self, training_data: pd.DataFrame) -> FootballModel:
        """Train a new model with fresh data"""
        # Prepare features and targets
        X, y = self.prepare_training_data(training_data)
        
        # Create and train new model
        model = FootballModel("xgboost")
        model.train(X, y)
        model.version = f"1.0.{int(datetime.utcnow().timestamp())}"
        
        # Save the model
        model_filepath = os.path.join(
            self.model_path, 
            f"football_model_{model.version}.joblib"
        )
        model.save(model_filepath)
        
        # Update current model
        self.current_model = model
        
        return model
    
    def load_latest_model(self) -> FootballModel:
        """Load the latest model from disk"""
        model_files = [f for f in os.listdir(self.model_path) if f.endswith('.joblib')]
        
        if not model_files:
            return None
        
        # Sort by modification time, get latest
        latest_file = max(
            model_files, 
            key=lambda f: os.path.getmtime(os.path.join(self.model_path, f))
        )
        
        filepath = os.path.join(self.model_path, latest_file)
        self.current_model = FootballModel.load(filepath)
        
        return self.current_model
    
    def prepare_training_data(self, data: pd.DataFrame) -> tuple:
        """Prepare training data from raw match data"""
        # Mock implementation - replace with actual feature engineering
        features = []
        targets = []
        
        for _, row in data.iterrows():
            # Mock feature extraction
            feature_vector = [
                row.get('home_team_avg_goals', 1.5),
                row.get('away_team_avg_goals', 1.2),
                row.get('home_advantage', 0.3),
                row.get('head_to_head_home_wins', 0.5),
                row.get('recent_form_home', 0.6),
                row.get('recent_form_away', 0.4),
                row.get('days_since_last_match', 7),
                row.get('league_competitiveness', 0.7),
                row.get('season_progress', 0.5),
                row.get('weather_factor', 0.5)
            ]
            
            target_vector = [row['home_score'], row['away_score']]
            
            features.append(feature_vector)
            targets.append(target_vector)
        
        return np.array(features), np.array(targets)
    
    def get_model_performance(self) -> Dict[str, Any]:
        """Get performance metrics of current model"""
        if self.current_model is None:
            return {"error": "No model loaded"}
        
        return {
            "version": self.current_model.version,
            "trained_at": self.current_model.trained_at.isoformat() if self.current_model.trained_at else None,
            "model_type": self.current_model.model_type,
            "performance_metrics": self.current_model.performance_metrics
        }