# app/memory.py

from app import google_maps

trip_memory = {
    "destination": "",
    "purpose": "",
}

def start_trip(destination: str, purpose: str):
    trip_memory["destination"] = destination
    trip_memory["purpose"] = purpose
    return trip_memory

def get_trip_summary():
    return f"You left to go to {trip_memory['destination']} for {trip_memory['purpose']}."

def get_current_location():
    return google_maps.get_current_location()

# Add to app/memory.py

# Example of simple in-memory storage
# app/memory.py

_trip_data = {}

def start_trip(destination, purpose):
    _trip_data["destination"] = destination
    _trip_data["purpose"] = purpose
    return _trip_data

def save_trip_coordinates(lat, lng):
    _trip_data["lat"] = lat
    _trip_data["lng"] = lng

def get_current_trip():
    return _trip_data