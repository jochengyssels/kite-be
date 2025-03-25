import os
import asyncio
import logging
from ..lib.ecmwf_client import ECMWFClient
from ..lib.neuralgcm_wrapper import NeuralGCMWrapper
import aiohttp
from datetime import datetime
from typing import List, Tuple
from ..models.weather import WeatherResponse, Location, WeatherData, Values, BatchWeatherResponse

logger = logging.getLogger(__name__)

class WeatherService:
    def __init__(self):
        self.use_neuralgcm = os.getenv("USE_NEURALGCM", "false").lower() == "true"
        self.ecmwf = ECMWFClient() if not self.use_neuralgcm else None
        self.gcm = NeuralGCMWrapper() if self.use_neuralgcm else None
        self.popular_destinations = [
            {
                "name": "Tarifa",
                "location": "Spain",
                "coordinates": {"lat": 36.0128, "lon": -5.6012}
            },
            {
                "name": "Cabarete",
                "location": "Dominican Republic",
                "coordinates": {"lat": 19.7667, "lon": -70.4167}
            },
            {
                "name": "Maui",
                "location": "USA",
                "coordinates": {"lat": 20.7984, "lon": -156.3319}
            }
        ]

    async def enhance_forecast(self, lat: float, lon: float):
        """Get enhanced forecast from selected backend"""
        try:
            if self.use_neuralgcm:
                # Run synchronous NeuralGCM code in thread pool
                return await asyncio.to_thread(
                    self._neuralgcm_prediction, 
                    lat, 
                    lon
                )
            return await self._ecmwf_prediction(lat, lon)
        except Exception as e:
            logger.error(f"Enhancement failed: {str(e)}")
            return {"error": str(e), "source": "none"}

    def _neuralgcm_prediction(self, lat: float, lon: float):
        """Synchronous wrapper for NeuralGCM"""
        try:
            return {
                "source": "NeuralGCM",
                **self.gcm.predict(lat, lon)
            }
        except Exception as e:
            logger.error(f"NeuralGCM prediction failed: {str(e)}")
            return {"error": str(e), "source": "NeuralGCM"}

    async def _ecmwf_prediction(self, lat: float, lon: float):
        """Async ECMWF prediction"""
        try:
            return {
                "source": "ECMWF",
                **await self.ecmwf.get_wind_data(lat, lon)
            }
        except Exception as e:
            logger.error(f"ECMWF prediction failed: {str(e)}")
            return {"error": str(e), "source": "ECMWF"}

    async def get_realtime_weather(self, lat: float, lon: float, tomorrow_api_key: str, weatherbit_api_key: str) -> WeatherResponse:
        """Get realtime weather data, trying Tomorrow.io first and falling back to Weatherbit."""
        try:
            # Try Tomorrow.io first
            tomorrow_data = await self._get_tomorrow_weather(lat, lon, tomorrow_api_key)
            if tomorrow_data:
                return tomorrow_data
        except Exception as e:
            logger.warning(f"Tomorrow.io API failed: {str(e)}")
        
        # Fallback to Weatherbit
        try:
            return await self._get_weatherbit_weather(lat, lon, weatherbit_api_key)
        except Exception as e:
            logger.error(f"Both weather APIs failed: {str(e)}")
            raise Exception("Failed to fetch weather data from both Tomorrow.io and Weatherbit")

    async def _get_tomorrow_weather(self, lat: float, lon: float, api_key: str) -> WeatherResponse:
        """Get weather data from Tomorrow.io API."""
        url = f"https://api.tomorrow.io/v4/weather/realtime?location={lat},{lon}&apikey={api_key}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise Exception(f"Tomorrow.io API error: {response.status}")
                
                data = await response.json()
                weather_data = data["data"]["values"]
                
                return WeatherResponse(
                    location=Location(
                        lat=lat,
                        lon=lon,
                        name=f"{lat}, {lon}"
                    ),
                    data=WeatherData(
                        time=datetime.utcnow().isoformat(),
                        values=Values(
                            temperature=weather_data["temperature"],
                            windSpeed=weather_data["windSpeed"],
                            windDirection=weather_data["windDirection"],
                            precipitationIntensity=weather_data.get("precipitationIntensity"),
                            humidity=weather_data.get("humidity"),
                            pressureSurfaceLevel=weather_data.get("pressureSurfaceLevel"),
                            visibility=weather_data.get("visibility"),
                            cloudCover=weather_data.get("cloudCover"),
                            uvIndex=weather_data.get("uvIndex")
                        )
                    )
                )

    async def _get_weatherbit_weather(self, lat: float, lon: float, api_key: str) -> WeatherResponse:
        """Get weather data from Weatherbit API."""
        url = f"https://api.weatherbit.io/v2.0/current?lat={lat}&lon={lon}&key={api_key}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise Exception(f"Weatherbit API error: {response.status}")
                
                data = await response.json()
                weather_data = data["data"][0]
                
                return WeatherResponse(
                    location=Location(
                        lat=lat,
                        lon=lon,
                        name=f"{lat}, {lon}"
                    ),
                    data=WeatherData(
                        time=datetime.utcnow().isoformat(),
                        values=Values(
                            temperature=weather_data["temp"],
                            windSpeed=weather_data["wind_spd"],
                            windDirection=weather_data["wind_dir"],
                            precipitationIntensity=weather_data.get("precip"),
                            humidity=weather_data.get("rh"),
                            pressureSurfaceLevel=weather_data.get("pres"),
                            visibility=weather_data.get("vis"),
                            cloudCover=weather_data.get("clouds"),
                            uvIndex=weather_data.get("uv")
                        )
                    )
                )

    async def get_batch_weather(self, tomorrow_api_key: str, weatherbit_api_key: str) -> BatchWeatherResponse:
        """Get weather data for multiple popular destinations."""
        weather_promises = [
            self.get_realtime_weather(
                dest["coordinates"]["lat"],
                dest["coordinates"]["lon"],
                tomorrow_api_key,
                weatherbit_api_key
            )
            for dest in self.popular_destinations
        ]
        
        results = await asyncio.gather(*weather_promises, return_exceptions=True)
        
        # Filter out any errors and format the response
        valid_results = [
            result for result in results
            if not isinstance(result, Exception)
        ]
        
        return BatchWeatherResponse(
            data=valid_results,
            _meta={"source": "tomorrow.io/weatherbit"}
        )
