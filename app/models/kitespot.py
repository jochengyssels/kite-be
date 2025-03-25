from pydantic import BaseModel
from typing import List, Optional

class Coordinates(BaseModel):
    lat: float
    lng: float

class KiteSpot(BaseModel):
    id: str
    name: str
    location: str
    country: str
    coordinates: Coordinates
    description: str
    bestFor: List[str]
    windDirection: List[str]
    waterConditions: str
    bestSeason: str
    difficulty: Optional[str] = None
    water_type: Optional[str] = None
    facilities: Optional[List[str]] = None
    best_months: Optional[List[str]] = None
    wave_spot: Optional[bool] = None
    flat_water: Optional[bool] = None
    suitable_for_beginners: Optional[bool] = None
    probability: Optional[float] = None
    wind_reliability: Optional[float] = None
    water_quality: Optional[float] = None
    crowd_level: Optional[float] = None
    overall_rating: Optional[float] = None 