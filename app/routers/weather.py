from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from ..services.weather_service import WeatherService
from ..models.weather import WeatherResponse, BatchWeatherResponse
from ..config import get_settings

router = APIRouter(prefix="/api/weather", tags=["weather"])
weather_service = WeatherService()

@router.get("/realtime", response_model=WeatherResponse)
async def get_realtime_weather(
    lat: float = Query(...),
    lon: float = Query(...),
    settings = get_settings()
):
    """Get realtime weather data for a location."""
    try:
        return await weather_service.get_realtime_weather(
            lat, 
            lon, 
            settings.tomorrow_api_key,
            settings.weatherbit_api_key
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/batch", response_model=BatchWeatherResponse)
async def get_batch_weather(settings = get_settings()):
    """Get weather data for multiple popular destinations."""
    try:
        return await weather_service.get_batch_weather(
            settings.tomorrow_api_key,
            settings.weatherbit_api_key
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
