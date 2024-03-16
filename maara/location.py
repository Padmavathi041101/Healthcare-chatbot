import os
import  requests
import geocoder, asyncio
import numpy as np
from geopy.distance import geodesic

def find_address(latitude, longitude):
    g = geocoder.osm([latitude, longitude], method='reverse')
    return g.address

def get_location_coordinates(location_keyword):
    try:
        api_key =os.environ.get("GOOGLE_MAP_API_KEY")
        if not api_key:
            raise ValueError("Google Maps API key not found in environment variables.")

        # Google Maps Geocoding API endpoint
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        # Parameters for the API request
        params = {
            "address": location_keyword,
            "key": api_key
        }
        # Sending the API request
        response = requests.get(url, params=params)
        data = response.json()
        
        # Checking if the request was successful
        if response.status_code == 200 and data["status"] == "OK":
            # Extracting latitude and longitude from the response
            latitude = data["results"][0]["geometry"]["location"]["lat"]
            longitude = data["results"][0]["geometry"]["location"]["lng"]
            return latitude, longitude
        else:
            print(f"Error: {data['status']}")
            return None, None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None, None


def find_location(latitude, longitude):
    if (latitude is None or longitude is None or 
        not -90 <= latitude <= 90 or 
        not -180 <= longitude <= 180 or 
        (latitude == 0 and longitude == 0)):
        return "unknown", "unknown"  
    g = geocoder.osm([latitude, longitude], method='reverse')
    if g.ok: 
        city_or_town_or_county = g.city if g.city else g.town if g.town else g.county
        state_or_province = g.state if g.state else g.state_district
        return city_or_town_or_county, state_or_province
    else:
        return "unknown", "unknown" 
