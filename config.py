import os
from dotenv import load_dotenv
from pydantic import BaseSettings

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings."""
    # API Keys
    groq_api_key: str = os.getenv("GROQ_API_KEY", "gsk_RKeG7qd7lpOxnK2k9EHpWGdyb3FYICtRBvXSfMfiFdfZlwjpUQ6")
    weatherbit_api_key: str = os.getenv("WEATHERBIT_API_KEY", "09b83eefa6ee49a58f535740e7e73528")
    tomorrow_api_key: str = os.getenv("TOMORROW_API_KEY", "zbtDpBoMzGlylEh5tblXugBsjkTyfw2S")
    locationiq_api_key: str = os.getenv("LOCATIONIQ_API_KEY", "pk.7d195946b1d5836bbef50b02dc8a4a41")
    maptiler_api_key: str = os.getenv("MAPTILER_API_KEY", "tVjXN27gMACKRAmwmC1v")
    
    # URLs
    iksurfmag_feed_url: str = os.getenv("IKSURFMAG_FEED_URL", "https://www.iksurfmag.com/feed/")
    
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

