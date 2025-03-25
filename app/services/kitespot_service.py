from typing import List, Optional
from ..models.kitespot import KiteSpot, Coordinates

class KiteSpotService:
    def __init__(self):
        # Initialize with some example data
        self.spots = [
            KiteSpot(
                id="tarifa",
                name="Tarifa Beach",
                location="Tarifa, Spain",
                country="Spain",
                coordinates=Coordinates(lat=36.0128, lng=-5.6012),
                description="Tarifa is known for its strong and consistent winds, making it a paradise for kitesurfers.",
                bestFor=["Advanced", "Intermediate"],
                windDirection=["East", "West"],
                waterConditions="Waves",
                bestSeason="Summer",
                difficulty="Advanced",
                water_type="Wave",
                wave_spot=True,
                wind_reliability=0.9,
                water_quality=0.8,
                crowd_level=0.7,
                overall_rating=0.85
            ),
            KiteSpot(
                id="cabarete",
                name="Cabarete",
                location="Puerto Plata, Dominican Republic",
                country="Dominican Republic",
                coordinates=Coordinates(lat=19.7667, lng=-70.4167),
                description="Cabarete offers a variety of conditions, from flat water lagoons to wave spots, suitable for all levels.",
                bestFor=["Beginner", "Intermediate", "Advanced"],
                windDirection=["East"],
                waterConditions="Flat Water & Waves",
                bestSeason="Winter",
                difficulty="Mixed",
                water_type="Mixed",
                wave_spot=True,
                flat_water=True,
                suitable_for_beginners=True,
                wind_reliability=0.85,
                water_quality=0.9,
                crowd_level=0.6,
                overall_rating=0.9
            ),
            KiteSpot(
                id="maui",
                name="Maui",
                location="Hawaii, USA",
                country="USA",
                coordinates=Coordinates(lat=20.7984, lng=-156.3319),
                description="Maui is a world-class kitesurfing destination with consistent trade winds and warm waters.",
                bestFor=["Intermediate", "Advanced"],
                windDirection=["Northeast"],
                waterConditions="Waves",
                bestSeason="Summer",
                difficulty="Advanced",
                water_type="Wave",
                wave_spot=True,
                wind_reliability=0.95,
                water_quality=0.9,
                crowd_level=0.8,
                overall_rating=0.95
            )
        ]

    def get_all_spots(self) -> List[KiteSpot]:
        """Get all kitespots."""
        return self.spots

    def get_spot_by_id(self, spot_id: str) -> Optional[KiteSpot]:
        """Get a specific kitespot by ID."""
        return next((spot for spot in self.spots if spot.id == spot_id), None)

    def get_spots_by_country(self, country: str) -> List[KiteSpot]:
        """Get all kitespots in a specific country."""
        return [spot for spot in self.spots if spot.country.lower() == country.lower()]

    def get_spots_by_difficulty(self, difficulty: str) -> List[KiteSpot]:
        """Get all kitespots with a specific difficulty level."""
        return [spot for spot in self.spots if spot.difficulty and spot.difficulty.lower() == difficulty.lower()]

    def get_spots_by_water_type(self, water_type: str) -> List[KiteSpot]:
        """Get all kitespots with a specific water type."""
        return [spot for spot in self.spots if spot.water_type and spot.water_type.lower() == water_type.lower()] 