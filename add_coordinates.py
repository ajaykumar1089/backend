#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.bikes.models import PickupLocation, BikeCity

# Sample coordinates for Indian cities (approximate lat/lng)
city_coordinates = {
    'Mumbai': (19.0760, 72.8777),
    'Delhi': (28.7041, 77.1025),
    'Bangalore': (12.9716, 77.5946),
    'Goa': (15.2993, 74.1240),
    'Pune': (18.5204, 73.8567),
    'Chennai': (13.0827, 80.2707),
    'Jaipur': (26.9124, 75.7873),
    'Kochi': (9.9312, 76.2673),
    'Manali': (32.2432, 77.1892),
    'Leh': (34.1526, 77.5771),
    'Mysore': (12.2958, 76.6394),
    'Udaipur': (24.5854, 73.7125),
}

def add_coordinates_to_locations():
    pickup_locations = PickupLocation.objects.all()
    
    print(f"Found {pickup_locations.count()} pickup locations")
    
    for location in pickup_locations:
        city_name = location.city.name
        print(f"Processing location: {location.name} in {city_name}")
        
        # Look for coordinates based on city name
        for city, coords in city_coordinates.items():
            if city.lower() in city_name.lower():
                location.latitude = coords[0]
                location.longitude = coords[1]
                location.save()
                print(f"  → Updated {location.name} with coordinates: {coords}")
                break
        else:
            print(f"  → No coordinates found for city: {city_name}")

if __name__ == '__main__':
    add_coordinates_to_locations()
    print("Coordinate update complete!")