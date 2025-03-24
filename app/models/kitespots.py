from fastapi import APIRouter, Query, HTTPException
import sqlite3
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import os
import logging
from datetime import datetime, timedelta
import random
import math

router = APIRouter()
logger = logging.getLogger(__name__)

# Database path
DB_PATH = 'data/kitespots.db'

class KitespotSuggestion(BaseModel):
    id: int
    name: str
    location: str
    country: Optional[str] = None

class KiteSpot(BaseModel):
    id: int
    name: str
    location: str
    coordinates: Optional[str] = None
    wind_speed: float
    wind_direction: int
    temperature: Optional[float] = None
    gust: Optional[float] = None
    difficulty: str
    water_type: str
    description: str
    image_url: str
    rating: Optional[float] = None
    review_count: Optional[int] = None
    facilities: Optional[List[str]] = None
    hazards: Optional[List[str]] = None

class SpotForecast(BaseModel):
    time: str
    wind_speed: float
    wind_direction: int
    temperature: float
    gust: float
    precipitation_probability: float

class GoldenKiteWindow(BaseModel):
    start_time: str
    end_time: str
    score: float

class SpotForecastResponse(BaseModel):
    forecast: List[SpotForecast]
    golden_kitewindow: Optional[GoldenKiteWindow] = None

@router.get("/api/kitespot-suggestions", response_model=List[KitespotSuggestion])
async def get_kitespot_suggestions(q: str = Query(..., min_length=1)):
    """
    Get kitespot suggestions based on search query.
    This endpoint is used for autocomplete functionality.
    """
    # Connect to the database
    if not os.path.exists(DB_PATH):
        logger.error(f"Database file not found at {DB_PATH}")
        return []
        
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # This enables column access by name
        cursor = conn.cursor()
        
        # Search for kitespots that match the query
        search_term = f"%{q.lower()}%"
        cursor.execute('''
        SELECT id, name, location, country
        FROM kitespots
        WHERE search_text LIKE ?
        ORDER BY 
            CASE 
                WHEN name LIKE ? THEN 1
                WHEN location LIKE ? THEN 2
                ELSE 3
            END,
            name
        LIMIT 10
        ''', (search_term, f"{q}%", f"{q}%"))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        # Format results for display
        suggestions = []
        for row in results:
            location_parts = []
            if row['location']:
                location_parts.append(row['location'])
            if row['country']:
                location_parts.append(row['country'])
            
            location_str = ", ".join(location_parts)
            
            suggestions.append(KitespotSuggestion(
                id=row['id'],
                name=row['name'],
                location=location_str,
                country=row['country']
            ))
        
        return suggestions
    except Exception as e:
        logger.error(f"Error fetching kitespot suggestions: {str(e)}")
        return []

@router.get("/api/spots", response_model=List[KiteSpot])
async def get_spots():
    """
    Get all kitespots with current conditions.
    """
    if not os.path.exists(DB_PATH):
        logger.error(f"Database file not found at {DB_PATH}")
        raise HTTPException(status_code=404, detail="Kitespot database not found")
        
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT id, name, location, country, latitude, longitude, difficulty, water_type
        FROM kitespots
        LIMIT 50
        ''')
        
        spots = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        # Add simulated weather data and other required fields
        result = []
        for spot in spots:
            # Generate random but realistic weather data
            wind_speed = round(random.uniform(8, 25), 1)
            wind_direction = random.randint(0, 359)
            temperature = round(random.uniform(15, 30), 1)
            gust = round(wind_speed * random.uniform(1.1, 1.4), 1)
            
            # Generate a description if none exists
            description = f"{spot['name']} is a popular kitesurfing spot located in {spot['location']}, {spot['country']}. " \
                         f"It features {spot['water_type'].lower()} water conditions and is suitable for {spot['difficulty'].lower()} riders."
            
            # Format coordinates as string
            coordinates = f"{spot['latitude']},{spot['longitude']}" if spot['latitude'] and spot['longitude'] else None
            
            # Create a complete spot object
            result.append(KiteSpot(
                id=spot['id'],
                name=spot['name'],
                location=f"{spot['location']}, {spot['country']}",
                coordinates=coordinates,
                wind_speed=wind_speed,
                wind_direction=wind_direction,
                temperature=temperature,
                gust=gust,
                difficulty=spot['difficulty'] or "Intermediate",
                water_type=spot['water_type'] or "Flat",
                description=description,
                image_url=f"/placeholder.svg?height=400&width=600&text={spot['name']}",
                rating=round(random.uniform(3.5, 5.0), 1),
                review_count=random.randint(10, 200),
                facilities=random.sample(["Parking", "Rentals", "Schools", "Restaurants", "Showers", "Toilets", "Accommodation"], 
                                        random.randint(2, 5)),
                hazards=random.sample(["Strong currents", "Shallow areas", "Rocks", "Boat traffic", "Jellyfish"], 
                                     random.randint(0, 3))
            ))
        
        return result
    except Exception as e:
        logger.error(f"Error fetching spots: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching spots: {str(e)}")

@router.get("/api/spots/featured", response_model=List[KiteSpot])
async def get_featured_spots():
    """
    Get featured kitespots.
    """
    # For simplicity, we'll just return the first 3 spots from the regular spots endpoint
    spots = await get_spots()
    return spots[:3]

@router.get("/api/spots/{spot_id}", response_model=KiteSpot)
async def get_spot_by_id(spot_id: int):
    """
    Get a specific kitespot by ID.
    """
    if not os.path.exists(DB_PATH):
        logger.error(f"Database file not found at {DB_PATH}")
        raise HTTPException(status_code=404, detail="Kitespot database not found")
        
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT id, name, location, country, latitude, longitude, difficulty, water_type
        FROM kitespots
        WHERE id = ?
        ''', (spot_id,))
        
        spot = cursor.fetchone()
        conn.close()
        
        if not spot:
            raise HTTPException(status_code=404, detail=f"Kitespot with ID {spot_id} not found")
        
        spot = dict(spot)
        
        # Generate random but realistic weather data
        wind_speed = round(random.uniform(8, 25), 1)
        wind_direction = random.randint(0, 359)
        temperature = round(random.uniform(15, 30), 1)
        gust = round(wind_speed * random.uniform(1.1, 1.4), 1)
        
        # Generate a description if none exists
        description = f"{spot['name']} is a popular kitesurfing spot located in {spot['location']}, {spot['country']}. " \
                     f"It features {spot['water_type'].lower() if spot['water_type'] else 'various'} water conditions and is suitable for " \
                     f"{spot['difficulty'].lower() if spot['difficulty'] else 'intermediate'} riders."
        
        # Format coordinates as string
        coordinates = f"{spot['latitude']},{spot['longitude']}" if spot['latitude'] and spot['longitude'] else None
        
        # Create a complete spot object
        return KiteSpot(
            id=spot['id'],
            name=spot['name'],
            location=f"{spot['location']}, {spot['country']}",
            coordinates=coordinates,
            wind_speed=wind_speed,
            wind_direction=wind_direction,
            temperature=temperature,
            gust=gust,
            difficulty=spot['difficulty'] or "Intermediate",
            water_type=spot['water_type'] or "Flat",
            description=description,
            image_url=f"/placeholder.svg?height=400&width=600&text={spot['name']}",
            rating=round(random.uniform(3.5, 5.0), 1),
            review_count=random.randint(10, 200),
            facilities=random.sample(["Parking", "Rentals", "Schools", "Restaurants", "Showers", "Toilets", "Accommodation"], 
                                    random.randint(2, 5)),
            hazards=random.sample(["Strong currents", "Shallow areas", "Rocks", "Boat traffic", "Jellyfish"], 
                                 random.randint(0, 3))
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching spot with ID {spot_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching spot: {str(e)}")

@router.get("/api/spots/{spot_id}/forecast", response_model=SpotForecastResponse)
async def get_spot_forecast(spot_id: int):
    """
    Get forecast data for a specific kitespot.
    """
    try:
        # Get the spot to ensure it exists
        spot = await get_spot_by_id(spot_id)
        
        # Generate a 3-day hourly forecast (72 hours)
        forecast = []
        start_time = datetime.now().replace(minute=0, second=0, microsecond=0)
        
        # Base wind speed and direction from the spot
        base_wind_speed = spot.wind_speed
        base_wind_direction = spot.wind_direction
        
        # Generate hourly forecast with realistic variations
        for i in range(72):
            forecast_time = start_time + timedelta(hours=i)
            
            # Add daily and hourly variations to make the forecast realistic
            day_factor = 1.0 + 0.2 * math.sin(2 * math.pi * (forecast_time.hour - 12) / 24)  # Peak at noon
            random_factor = random.uniform(0.8, 1.2)
            
            wind_speed = round(base_wind_speed * day_factor * random_factor, 1)
            wind_direction = (base_wind_direction + random.randint(-20, 20)) % 360
            temperature = round(spot.temperature + 5 * math.sin(2 * math.pi * (forecast_time.hour - 14) / 24), 1)  # Peak at 2pm
            gust = round(wind_speed * random.uniform(1.1, 1.5), 1)
            precip_prob = round(random.uniform(0, 30), 1)
            
            forecast.append(SpotForecast(
                time=forecast_time.isoformat(),
                wind_speed=wind_speed,
                wind_direction=wind_direction,
                temperature=temperature,
                gust=gust,
                precipitation_probability=precip_prob
            ))
        
        # Find the best window for kitesurfing (3-hour window with highest wind speeds in the ideal range)
        best_window_start = None
        best_window_end = None
        best_score = 0
        
        for i in range(len(forecast) - 3):
            window = forecast[i:i+3]
            
            # Calculate score based on wind speed (ideal is 15-20 knots)
            scores = []
            for hour in window:
                if 15 <= hour.wind_speed <= 20:
                    score = 1.0  # Perfect
                elif 12 <= hour.wind_speed < 15 or 20 < hour.wind_speed <= 25:
                    score = 0.7  # Good
                elif 8 <= hour.wind_speed < 12:
                    score = 0.4  # Fair
                else:
                    score = 0.2  # Poor
                scores.append(score)
            
            avg_score = sum(scores) / len(scores)
            
            if avg_score > best_score:
                best_score = avg_score
                best_window_start = window[0].time
                best_window_end = window[-1].time
        
        # Create golden kite window if a good window was found
        golden_window = None
        if best_score > 0.5:
            golden_window = GoldenKiteWindow(
                start_time=best_window_start,
                end_time=best_window_end,
                score=best_score
            )
        
        return SpotForecastResponse(
            forecast=forecast,
            golden_kitewindow=golden_window
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating forecast for spot {spot_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating forecast: {str(e)}")

@router.get("/api/current-conditions")
async def get_current_conditions():
    """
    Get current weather conditions and the nearest kitespot.
    """
    try:
        # Get a random spot to simulate the nearest spot
        spots = await get_spots()
        nearest_spot = random.choice(spots)
        
        # Generate current conditions
        wind_speed = round(random.uniform(8, 25), 1)
        wind_direction = random.randint(0, 359)
        temperature = round(random.uniform(15, 30), 1)
        
        return {
            "wind_speed": wind_speed,
            "wind_direction": wind_direction,
            "temperature": temperature,
            "nearest_spot": {
                "name": nearest_spot.name,
                "id": nearest_spot.id
            }
        }
    except Exception as e:
        logger.error(f"Error fetching current conditions: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching current conditions: {str(e)}")

