import os
from dotenv import load_dotenv
from pydantic import BaseSettings

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings."""
    # API Keys
    api_key_name1: str = os.getenv("API_KEY_NAME1", "")
    api_key_name2: str = os.getenv("API_KEY_NAME2", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    weather_api_key: str = os.getenv("WEATHER_API_KEY", "")
    
    # Other settings
    app_name: str = "Kite API"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    class Config:
        env_file = ".env"

# Create a global settings object
settings = Settings()

# Function to get settings
def get_settings():
    return settings

