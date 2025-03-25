from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import kitespots, weather
from app.config import get_settings, Settings

app = FastAPI(
    title="Kite API",
    description="API for kitesurfing spots and weather information",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "https://kite-fe.vercel.app",  # Vercel frontend
        "https://kiteaways.vercel.app",  # Alternative Vercel domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(kitespots.router)
app.include_router(weather.router)

@app.get("/")
async def read_root(settings: Settings = get_settings()):
    return {
        "app_name": settings.app_name,
        "version": "1.0.0",
        "status": "running"
    }

# Example of using an API key in an endpoint
@app.get("/weather/{location}")
async def get_weather(location: str, settings: Settings = get_settings()):
    # Here you would use settings.weather_api_key to make a request
    # to a weather API using the requests or aiohttp library
    return {"location": location, "forecast": "Example forecast"}

