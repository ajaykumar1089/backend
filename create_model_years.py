#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.bikes.models import Bike, BikeModelYear

def create_model_years():
    """Create BikeModelYear records for years 2000-2025 and update existing bikes"""
    
    print("Creating BikeModelYear records...")
    
    # Create model years from 2000 to 2025
    for year in range(2000, 2026):
        model_year, created = BikeModelYear.objects.get_or_create(year=year)
        if created:
            print(f"Created model year: {year}")
        else:
            print(f"Model year {year} already exists")
    
    print(f"\nTotal BikeModelYear records: {BikeModelYear.objects.count()}")
    
    # Note: The migration will handle updating existing bike records automatically
    # since we're changing the field from IntegerField to ForeignKey

if __name__ == '__main__':
    create_model_years()
    print("Model year setup complete!")