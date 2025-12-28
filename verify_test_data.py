#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.accounts.models import User
from apps.bikes.models import Bike, BikeCity, BikeBrand

print("=== TravellerClicks Test Data Verification ===\n")

# Check users
users = User.objects.all()
print(f"📊 Total Users: {users.count()}")
for user in users:
    print(f"  • {user.email} ({user.user_type}) - Verified: {user.is_verified}")

# Check bikes
bikes = Bike.objects.all()
print(f"\n🚲 Total Bikes: {bikes.count()}")
for bike in bikes:
    print(f"  • {bike.title} - ${bike.price_per_day}/day")
    print(f"    Provider: {bike.service_provider.email}")
    print(f"    City: {bike.city.name}")
    print(f"    Available: {'✅' if bike.available else '❌'}")

# Check supporting data
cities = BikeCity.objects.all()
brands = BikeBrand.objects.all()
print(f"\n🏙️ Cities: {cities.count()}")
for city in cities:
    print(f"  • {city.name}, {city.state}")

print(f"\n🏷️ Brands: {brands.count()}")
for brand in brands:
    print(f"  • {brand.name}")

print("\n✅ Test data verification complete!")
print("🔧 You can now test the booking functionality with these accounts:")
print("  - traveller@test.com (password: testpass123)")
print("  - provider@test.com (password: testpass123)")
print("  - admin@test.com (password: testpass123)")