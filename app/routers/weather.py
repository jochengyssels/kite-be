from fastapi import APIRouter, Query
from ..services.weather_service import WeatherService

router = APIRouter()
weather_service = WeatherService()

@router.get("/api/weather")
async def get_weather(lat: float = Query(...), lng: float = Query(...)):
    enhanced_forecast = weather_service.get_enhanced_forecast(lat, lng)
    return {
        "wind_speed": enhanced_forecast['wind_speed'],
        "wind_direction": enhanced_forecast['wind_direction'],
    }
