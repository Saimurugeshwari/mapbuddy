# app/google_maps.py
import os
import googlemaps
from dotenv import load_dotenv

load_dotenv()  # Load .env file for local development

GMAPS_API_KEY = os.getenv("GMAPS_API_KEY")
gmaps = googlemaps.Client(key=GMAPS_API_KEY)

#Mock current coordinates (simulate GPS for now)
# Later, this should be replaced with dynamic tracking.
current_location = {"lat": 28.6139, "lng": 77.2090}  # Example: New Delhi coordinates

def get_current_location():
    """Uses Google Maps Python client to get address from coordinates."""
    result = gmaps.reverse_geocode((current_location['lat'], current_location['lng']))

    if result:
        return result[0].get("formatted_address", "Address unavailable")
    else:
        return f"Latitude: {current_location['lat']}, Longitude: {current_location['lng']} (address unavailable)"

def update_location():
    """Simulate small movement in coordinates. In real app, you'd use device GPS."""
    current_location["lat"] += 0.0005  # Simulate northward movement
    current_location["lng"] += 0.0005  # Simulate eastward movement

def get_directions(origin, destination):
    directions_result = gmaps.directions(origin, destination)
    return directions_result
