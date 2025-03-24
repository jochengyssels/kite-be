from fastapi import FastAPI, Depends
from app.config import get_settings, Settings

app = FastAPI()

@app.get("/")
async def read_root(settings: Settings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
        "debug_mode": settings.debug
    }

# Example of using an API key in an endpoint
@app.get("/weather/{location}")
async def get_weather(location: str, settings: Settings = Depends(get_settings)):
    # Here you would use settings.weather_api_key to make a request
    # to a weather API using the requests or aiohttp library
    return {"location": location, "forecast": "Example forecast"}

