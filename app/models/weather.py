from pydantic import BaseModel

class WeatherResponse(BaseModel):
    wind_speed: list[float]
    wind_direction: list[float]
    optimal_window: tuple[str, str]
