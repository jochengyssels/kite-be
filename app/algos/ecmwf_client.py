import aiohttp
import numpy as np
from tenacity import retry, stop_after_attempt, wait_exponential

class ECMWFClient:
    BASE_URL = "https://api.open-meteo.com/v1/ecmwf"
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def get_wind_data(self, lat: float, lon: float):
        """Get 10m wind data from ECMWF OpenAPI"""
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "wind_speed_10m,wind_direction_10m",
            "wind_speed_unit": "kn",  # Knots for kitesurfing
            "forecast_days": 3,       # Optimal forecast window
            "timezone": "auto"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(self.BASE_URL, params=params) as response:
                data = await response.json()
                return self._parse_response(data)

    def _parse_response(self, data):
        """Convert API response to kitesurfing format"""
        return {
            "wind_speed": data["hourly"]["wind_speed_10m"],
            "wind_direction": data["hourly"]["wind_direction_10m"]
        }
