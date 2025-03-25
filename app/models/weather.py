from pydantic import BaseModel
from typing import List, Optional

class Values(BaseModel):
    temperature: float
    windSpeed: float
    windDirection: float
    precipitationIntensity: Optional[float] = None
    humidity: Optional[float] = None
    pressureSurfaceLevel: Optional[float] = None
    visibility: Optional[float] = None
    cloudCover: Optional[float] = None
    uvIndex: Optional[float] = None

class Location(BaseModel):
    lat: float
    lon: float
    name: str

class WeatherData(BaseModel):
    time: str
    values: Values

class WeatherResponse(BaseModel):
    location: Location
    data: WeatherData

class BatchWeatherResponse(BaseModel):
    data: List[WeatherResponse]
    _meta: dict
