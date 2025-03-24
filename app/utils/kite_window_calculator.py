from typing import List, Dict, Tuple
import numpy as np

def calculate_golden_kitewindow(forecast: List[Dict], window_size: int = 3) -> Tuple[str, str, float]:
    """
    Calculate the best kitesurfing window based on wind conditions.
    
    :param forecast: List of hourly forecast dictionaries
    :param window_size: Size of the window in hours
    :return: Tuple of (start_time, end_time, score)
    """
    scores = []
    for i in range(len(forecast) - window_size + 1):
        window = forecast[i:i+window_size]
        score = calculate_window_score(window)
        scores.append((i, score))
    
    best_window = max(scores, key=lambda x: x[1])
    start_index = best_window[0]
    
    start_time = forecast[start_index]['time']
    end_time = forecast[start_index + window_size - 1]['time']
    
    return start_time, end_time, best_window[1]

def calculate_window_score(window: List[Dict]) -> float:
    """
    Calculate a score for a given time window based on kitesurfing conditions.
    
    :param window: List of hourly forecast dictionaries for the time window
    :return: Score for the window
    """
    wind_speeds = [hour['windSpeed'] for hour in window]
    wind_directions = [hour['windDirection'] for hour in window]
    
    avg_speed = np.mean(wind_speeds)
    speed_consistency = 1 - np.std(wind_speeds) / avg_speed
    direction_consistency = 1 - np.std(wind_directions) / 180
    
    # Adjust these weights based on importance
    speed_weight = 0.5
    speed_consistency_weight = 0.3
    direction_consistency_weight = 0.2
    
    # Ideal wind speed range (adjust as needed)
    ideal_speed_low = 15
    ideal_speed_high = 25
    
    # Calculate speed score
    if avg_speed < ideal_speed_low:
        speed_score = avg_speed / ideal_speed_low
    elif avg_speed > ideal_speed_high:
        speed_score = 1 - (avg_speed - ideal_speed_high) / ideal_speed_high
    else:
        speed_score = 1
    
    # Calculate final score
    score = (
        speed_score * speed_weight +
        speed_consistency * speed_consistency_weight +
        direction_consistency * direction_consistency_weight
    )
    
    return score
