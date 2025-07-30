# app/utils.py
import os
import requests

def geocode_address(address: str):
    api_key = os.getenv("GMAPS_API_KEY")
    if not api_key:
        raise ValueError("Missing GMAPS_API_KEY in environment.")
    response = requests.get(
        "https://maps.googleapis.com/maps/api/geocode/json",
        params={"address": address, "key": api_key}
    )
    result = response.json()
    if result["status"] == "OK":
        location = result["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    return None, None
