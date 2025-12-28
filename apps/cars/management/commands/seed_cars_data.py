from django.core.management.base import BaseCommand
from apps.cars.models import (
    CarCity, CarTransmission, CarFuelType, CarType, CarBrand, CarModelYear
)

class Command(BaseCommand):
    help = 'Seed initial data for cars app'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting cars data seeding...'))

        # Create Car Cities (same as bikes)
        cities = [
            'Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad',
            'Pune', 'Ahmedabad', 'Surat', 'Jaipur', 'Lucknow', 'Kanpur',
            'Nagpur', 'Indore', 'Thane', 'Bhopal', 'Visakhapatnam', 'Pimpri-Chinchwad',
            'Patna', 'Vadodara', 'Ghaziabad', 'Ludhiana', 'Agra', 'Nashik',
            'Faridabad', 'Meerut', 'Rajkot', 'Kalyan-Dombivali', 'Vasai-Virar', 'Varanasi'
        ]
        for city_name in cities:
            CarCity.objects.get_or_create(
                name=city_name,
                defaults={'state': 'India', 'country': 'India'}
            )

        # Create Car Transmissions
        transmissions = [
            'Manual',
            'Automatic',
            'CVT',
            'AMT',
            'DCT'
        ]
        for transmission in transmissions:
            CarTransmission.objects.get_or_create(type=transmission)

        # Create Car Fuel Types
        fuel_types = [
            'Petrol',
            'Diesel',
            'Electric',
            'Hybrid',
            'CNG',
            'LPG'
        ]
        for fuel_type in fuel_types:
            CarFuelType.objects.get_or_create(type=fuel_type)

        # Create Car Types
        car_types = [
            'Hatchback',
            'Sedan',
            'SUV',
            'Crossover',
            'MPV',
            'Convertible',
            'Coupe',
            'Wagon',
            'Pickup',
            'Luxury'
        ]
        for car_type in car_types:
            CarType.objects.get_or_create(type=car_type)

        # Create Car Brands
        brands = [
            'Maruti Suzuki', 'Hyundai', 'Tata', 'Mahindra', 'Toyota', 'Honda',
            'Ford', 'Chevrolet', 'Nissan', 'Volkswagen', 'Skoda', 'Renault',
            'Kia', 'MG Motor', 'Jeep', 'BMW', 'Mercedes-Benz', 'Audi',
            'Volvo', 'Jaguar', 'Land Rover', 'Porsche', 'Lexus', 'Infiniti',
            'Citroen', 'Peugeot', 'Isuzu', 'Force Motors', 'Datsun'
        ]
        for brand_name in brands:
            CarBrand.objects.get_or_create(
                name=brand_name,
                defaults={'country': 'India' if brand_name in ['Maruti Suzuki', 'Tata', 'Mahindra', 'Force Motors'] else 'International'}
            )

        # Create Model Years
        current_year = 2024
        for year in range(2005, current_year + 2):
            CarModelYear.objects.get_or_create(year=year)

        self.stdout.write(self.style.SUCCESS('Successfully seeded cars data'))