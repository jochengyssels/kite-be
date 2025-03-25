from fastapi import APIRouter, HTTPException
from typing import List, Optional
from ..models.kitespot import KiteSpot
from ..services.kitespot_service import KiteSpotService

router = APIRouter(prefix="/api/kitespots", tags=["kitespots"])
kitespot_service = KiteSpotService()

@router.get("/", response_model=List[KiteSpot])
async def get_kitespots():
    """Get all kitespots."""
    return kitespot_service.get_all_spots()

@router.get("/{spot_id}", response_model=KiteSpot)
async def get_kitespot_by_id(spot_id: str):
    """Get a specific kitespot by ID."""
    spot = kitespot_service.get_spot_by_id(spot_id)
    if not spot:
        raise HTTPException(status_code=404, detail="Kitespot not found")
    return spot

@router.get("/country/{country}", response_model=List[KiteSpot])
async def get_spots_by_country(country: str):
    """Get all kitespots in a specific country."""
    return kitespot_service.get_spots_by_country(country)

@router.get("/difficulty/{difficulty}", response_model=List[KiteSpot])
async def get_spots_by_difficulty(difficulty: str):
    """Get all kitespots with a specific difficulty level."""
    return kitespot_service.get_spots_by_difficulty(difficulty)

@router.get("/water-type/{water_type}", response_model=List[KiteSpot])
async def get_spots_by_water_type(water_type: str):
    """Get all kitespots with a specific water type."""
    return kitespot_service.get_spots_by_water_type(water_type)