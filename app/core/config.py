from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    model_config = {
        "protected_namespaces": ("settings_",),
        "env_file": ".env"
    }
    
    app_name: str = "Football Prediction Service"
    debug: bool = False
    
    # Database
    database_url: Optional[str] = None
    
    # Redis
    redis_url: Optional[str] = None
    
    # External APIs
    football_api_key: Optional[str] = None
    football_api_url: str = "https://api.football-data.org/v4"
    
    # ML Model settings
    model_path: str = "models/"
    retrain_interval_hours: int = 24

settings = Settings()