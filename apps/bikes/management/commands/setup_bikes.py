from django.core.management.base import BaseCommand
from apps.bikes.models import (
    BikeCity, BikeBrand, BikeTransmission, BikeFuelType, 
    BikeRentalType, PickupLocation, Bike, BikeImage
)
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Setup bikes data with required relationships'

    def handle(self, *args, **options):
        self.stdout.write('Setting up bikes data...')
        
        # Clear existing bikes to ensure fresh data
        Bike.objects.all().delete()
        
        # Create or get a service provider user
        user, created = User.objects.get_or_create(
            username='service_provider_1',
            defaults={
                'email': 'provider@example.com',
                'first_name': 'Service',
                'last_name': 'Provider',
                'user_type': 'service_provider'
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            self.stdout.write(f'Created service provider user: {user.username}')
        
        # Create bike brands
        hero, _ = BikeBrand.objects.get_or_create(name='Hero')
        honda, _ = BikeBrand.objects.get_or_create(name='Honda')
        trek, _ = BikeBrand.objects.get_or_create(name='Trek')
        
        # Create cities
        mumbai, _ = BikeCity.objects.get_or_create(
            name='Mumbai', 
            defaults={'state': 'Maharashtra'}
        )
        delhi, _ = BikeCity.objects.get_or_create(
            name='Delhi', 
            defaults={'state': 'Delhi'}
        )
        la, _ = BikeCity.objects.get_or_create(
            name='Los Angeles', 
            defaults={'state': 'California'}
        )
        
        # Create transmission types
        gear, _ = BikeTransmission.objects.get_or_create(type='Gear')
        gearless, _ = BikeTransmission.objects.get_or_create(type='Gearless')
        manual, _ = BikeTransmission.objects.get_or_create(type='Manual')
        automatic, _ = BikeTransmission.objects.get_or_create(type='Automatic')
        
        # Create fuel types
        petrol, _ = BikeFuelType.objects.get_or_create(type='Petrol')
        cng, _ = BikeFuelType.objects.get_or_create(type='CNG')
        diesel, _ = BikeFuelType.objects.get_or_create(type='Diesel')
        electric, _ = BikeFuelType.objects.get_or_create(type='Electric')
        
        # Create rental types
        hours, _ = BikeRentalType.objects.get_or_create(type='Hours')
        days, _ = BikeRentalType.objects.get_or_create(type='Days')
        weeks, _ = BikeRentalType.objects.get_or_create(type='Weeks')
        months, _ = BikeRentalType.objects.get_or_create(type='Months')
        
        # Create pickup locations
        andheri, _ = PickupLocation.objects.get_or_create(
            name='Andheri',
            defaults={'address': 'Andheri West', 'city': mumbai}
        )
        bandra, _ = PickupLocation.objects.get_or_create(
            name='Bandra',
            defaults={'address': 'Bandra East', 'city': mumbai}
        )
        cp, _ = PickupLocation.objects.get_or_create(
            name='CP',
            defaults={'address': 'Connaught Place', 'city': delhi}
        )
        
        # Create bikes
        bike1 = Bike.objects.create(
            service_provider=user,
            title='City Cruiser Bike',
            model='City Cruiser',
            brand=trek,
            model_year=2022,
            city=la,
            transmission=manual,
            fuel_type=petrol,
            rental_type=days,
            engine_capacity='125cc',
            mileage='45 km/l',
            price_per_hour=35.00,
            price_per_day=280.00,
            safety_deposit=150.00,
            operating_hours='8:00 AM - 8:00 PM',
            available=True,
            documents_required='Valid ID and driving license',
            terms_and_conditions='Standard rental terms apply',
            description='Perfect for city rides and short trips',
            rating=4.2,
            total_reviews=45,
            total_trips=120
        )
        bike1.pickup_locations.add(andheri, bandra)
        self.stdout.write(f'Created bike: {bike1.title}')
        
        bike2 = Bike.objects.create(
            service_provider=user,
            title='Mountain Adventure Bike',
            model='Mountain Adventure',
            brand=trek,
            model_year=2023,
            city=la,
            transmission=manual,
            fuel_type=petrol,
            rental_type=days,
            engine_capacity='150cc',
            mileage='40 km/l',
            price_per_hour=50.00,
            price_per_day=400.00,
            safety_deposit=200.00,
            operating_hours='6:00 AM - 10:00 PM',
            available=True,
            documents_required='Valid ID and driving license',
            terms_and_conditions='Standard rental terms apply',
            description='Great for mountain trails and adventure rides',
            rating=4.7,
            total_reviews=78,
            total_trips=150
        )
        bike2.pickup_locations.add(cp)
        self.stdout.write(f'Created bike: {bike2.title}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully setup bikes data. Total bikes: {Bike.objects.count()}')
        )