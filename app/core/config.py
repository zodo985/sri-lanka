from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Application
    app_name: str = "Sri Lanka Tourism Chatbot API"
    version: str = "1.0.0"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Database
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "sri_lanka_tourism_chatbot"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # Security
    secret_key: str = "your_super_secret_key_here_change_this_in_production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    encryption_key: str = "your_32_character_encryption_key_here"
    salt_rounds: int = 12
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # External APIs
    google_maps_api_key: Optional[str] = None
    openweather_api_key: Optional[str] = None
    currency_layer_api_key: Optional[str] = None
    google_translate_api_key: Optional[str] = None
    google_speech_api_key: Optional[str] = None
    
    # Rasa
    rasa_server_url: str = "http://localhost:5005"
    rasa_webhook_url: str = "http://localhost:8000/webhooks/rasa"
    
    # Supported Languages
    supported_languages: List[str] = [
        "en", "si", "ta", "de", "fr", "zh", "ja"
    ]
    
    # Language Names
    language_names: dict = {
        "en": "English",
        "si": "සිංහල",
        "ta": "தமிழ்",
        "de": "Deutsch",
        "fr": "Français",
        "zh": "中文",
        "ja": "日本語"
    }
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()