from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.accounts.models import User
from apps.bikes.models import Bike, BikeBrand, BikeCity, BikeTransmission, BikeFuelType, BikeRentalType, PickupLocation

class Command(BaseCommand):
    help = 'Create sample service data for testing TravellerClicks functionality'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample service data...'))
        
        # Get the service provider user
        try:
            provider = User.objects.get(email='provider@test.com')
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Service provider not found. Please run create_test_users first.')
            )
            return

        # Create supporting data first
        city, _ = BikeCity.objects.get_or_create(
            name='Los Angeles',
            defaults={'state': 'California', 'country': 'USA'}
        )
        
        brand, _ = BikeBrand.objects.get_or_create(name='Trek')
        transmission, _ = BikeTransmission.objects.get_or_create(type='Manual')
        fuel_type, _ = BikeFuelType.objects.get_or_create(type='Petrol')
        rental_type, _ = BikeRentalType.objects.get_or_create(type='Self Drive')
        
        pickup_location, _ = PickupLocation.objects.get_or_create(
            name='Downtown LA Hub',
            defaults={
                'address': '123 Main St, Downtown LA',
                'city': city
            }
        )

        # Create sample bikes
        sample_bikes = [
            {
                'title': 'Mountain Adventure Bike',
                'model': 'X-Caliber 8',
                'brand': brand,
                'model_year': 2023,
                'city': city,
                'transmission': transmission,
                'fuel_type': fuel_type,
                'rental_type': rental_type,
                'price_per_hour': '10.00',
                'price_per_day': '50.00',
                'safety_deposit': '200.00',
                'service_provider': provider,
                'operating_hours': '9 AM - 8 PM',
                'available': True,
                'documents_required': 'Valid driving license, Aadhar card',
                'terms_and_conditions': 'Must return in same condition. Late fees apply.',
                'description': 'Perfect for mountain trails and adventure rides. High-quality suspension and durable frame.',
                'rating': '4.5'
            },
            {
                'title': 'City Cruiser Bike',
                'model': 'Escape 3',
                'brand': brand,
                'model_year': 2022,
                'city': city,
                'transmission': transmission,
                'fuel_type': fuel_type,
                'rental_type': rental_type,
                'price_per_hour': '7.00',
                'price_per_day': '35.00',
                'safety_deposit': '150.00',
                'service_provider': provider,
                'operating_hours': '8 AM - 9 PM',
                'available': True,
                'documents_required': 'Valid driving license, ID proof',
                'terms_and_conditions': 'No smoking, return with full tank.',
                'description': 'Comfortable city bike perfect for urban exploration and daily commutes.',
                'rating': '4.2'
            }
        ]

        for bike_data in sample_bikes:
            try:
                bike, created = Bike.objects.get_or_create(
                    title=bike_data['title'],
                    service_provider=provider,
                    defaults=bike_data
                )
                if created:
                    # Add pickup location
                    bike.pickup_locations.add(pickup_location)
                    self.stdout.write(
                        self.style.SUCCESS(f'Created bike: {bike.title}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Bike already exists: {bike.title}')
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating bike {bike_data["title"]}: {e}')
                )

        self.stdout.write(self.style.SUCCESS('\n=== Sample Data Created ==='))
        self.stdout.write(f'✅ Sample bikes added to provider account')
        self.stdout.write(f'🔑 Provider: {provider.email}')
        self.stdout.write(f'🏙️ City: {city.name}')
        self.stdout.write(f'📍 Pickup Location: {pickup_location.name}')
        self.stdout.write(self.style.SUCCESS('\nYou can now test booking functionality!'))