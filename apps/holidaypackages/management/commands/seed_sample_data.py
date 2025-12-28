from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date, timedelta

# Import all models for seeding
from apps.bikes.models import Bike, BikeImage, BikeAvailability, BikeReview, BikeModelYear
from apps.cars.models import Car, CarImage, CarAvailability, CarReview, CarModelYear
from apps.campervans.models import Campervan, CampervanImage, CampervanAvailability, CampervanReview, CampervanModelYear
from apps.hotels.models import Hotel, HotelImage, HotelAvailability, HotelReview
from apps.guided_trips.models import GuidedTrip, TripImage, TripParticipant
from apps.pilgrim.models import PilgrimTour, PilgrimHotel, PilgrimageDestination, PilgrimTourImage, PilgrimHotelImage
from apps.stories.models import UserStory, StoryImage, StoryLike, StoryComment
from apps.insights.models import TravelInsight, InsightLike, InsightComment

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed sample data for all tables'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting sample data seeding...'))

        # Create sample users
        service_provider1, _ = User.objects.get_or_create(
            email='provider1@example.com',
            defaults={
                'username': 'bikeprovider1',
                'user_type': 'service_provider',
                'firm_name': 'Mumbai Bike Rentals',
                'phone_number': '+91-9876543210',
                'is_verified': True
            }
        )

        service_provider2, _ = User.objects.get_or_create(
            email='provider2@example.com',
            defaults={
                'username': 'carprovider1',
                'user_type': 'service_provider',
                'firm_name': 'Delhi Car Rentals',
                'phone_number': '+91-9876543211',
                'is_verified': True
            }
        )

        traveller1, _ = User.objects.get_or_create(
            email='traveller1@example.com',
            defaults={
                'username': 'traveller1',
                'user_type': 'traveller',
                'phone_number': '+91-9876543212',
                'is_verified': True
            }
        )

        traveller2, _ = User.objects.get_or_create(
            email='traveller2@example.com',
            defaults={
                'username': 'traveller2',
                'user_type': 'traveller',
                'phone_number': '+91-9876543213',
                'is_verified': True
            }
        )

        # Import required models for relationships
        from apps.bikes.models import BikeCity, BikeBrand, BikeFuelType, BikeTransmission, BikeModelYear, BikeRentalType
        from apps.cars.models import CarCity, CarBrand, CarFuelType, CarTransmission, CarModelYear, CarType
        from apps.campervans.models import CampervanCity, CampervanBrand, CampervanFuelType, CampervanTransmission, CampervanModelYear, CampervanToilet, CampervanShower
        from apps.hotels.models import HotelCity, PropertyType, BedPreference, ReservationType
        from apps.guided_trips.models import TripRegion, TripCity, TripType, TripDifficultyLevel, JoinType
        from apps.pilgrim.models import PilgrimRegion, PilgrimPackageType, PilgrimDifficultyLevel
        from apps.stories.models import StoryCity, StoryPlaceType, StoryJourneyType
        from apps.insights.models import InsightCategory

        # Create rental types if they don't exist
        for rental_type in ['Hourly', 'Daily', 'Weekly', 'Monthly']:
            BikeRentalType.objects.get_or_create(type=rental_type)

        # Create sample bikes
        mumbai = BikeCity.objects.first()
        hero_brand = BikeBrand.objects.filter(name__icontains='Hero').first()
        petrol_fuel = BikeFuelType.objects.filter(type='Petrol').first()
        manual_trans = BikeTransmission.objects.filter(type='Manual').first()
        year_2022 = BikeModelYear.objects.filter(year=2022).first()
        hourly_rental = BikeRentalType.objects.filter(type='Hourly').first()

        if all([mumbai, hero_brand, petrol_fuel, manual_trans, year_2022, hourly_rental]):
            bike1, created = Bike.objects.get_or_create(
                title='Hero Splendor Plus',
                defaults={
                    'model': 'Splendor Plus',
                    'description': 'Reliable and fuel-efficient bike perfect for city rides',
                    'city': mumbai,
                    'brand': hero_brand,
                    'fuel_type': petrol_fuel,
                    'transmission': manual_trans,
                    'rental_type': hourly_rental,
                    'model_year': year_2022,
                    'service_provider': service_provider1,
                    'price_per_hour': Decimal('150.00'),
                    'price_per_day': Decimal('1200.00'),
                    'engine_capacity': '97cc',
                    'mileage': '80 kmpl',
                    'safety_deposit': Decimal('5000.00'),
                    'operating_hours': '6 AM - 10 PM',
                    'documents_required': 'Valid driving license',
                    'terms_and_conditions': 'Standard rental terms apply',
                    'rating': Decimal('4.2'),
                    'total_trips': 25,
                    'available': True
                }
            )

        # Create sample cars
        delhi = CarCity.objects.first()
        maruti_brand = CarBrand.objects.filter(name__icontains='Maruti').first()
        car_petrol = CarFuelType.objects.filter(type='Petrol').first()
        car_manual = CarTransmission.objects.filter(type='Manual').first()
        hatchback = CarType.objects.filter(type='Hatchback').first()
        car_year_2022 = CarModelYear.objects.filter(year=2022).first()

        if all([delhi, maruti_brand, car_petrol, car_manual, hatchback, car_year_2022]):
            car1, created = Car.objects.get_or_create(
                title='Maruti Swift',
                defaults={
                    'model': 'Swift VXI',
                    'description': 'Compact and efficient car perfect for city driving',
                    'city': delhi,
                    'brand': maruti_brand,
                    'fuel_type': car_petrol,
                    'transmission': car_manual,
                    'vehicle_type': hatchback,
                    'model_year': car_year_2022,
                    'service_provider': service_provider2,
                    'price_per_hour': Decimal('300.00'),
                    'price_per_day': Decimal('2400.00'),
                    'seating_capacity': 5,
                    'engine_capacity': '1197cc',
                    'mileage': '23 kmpl',
                    'baggage_capacity': 268,
                    'safety_deposit': Decimal('10000.00'),
                    'operating_hours': '9 AM - 9 PM',
                    'documents_required': 'Valid driving license, Aadhaar card',
                    'terms_and_conditions': 'Standard rental terms apply',
                    'rating': Decimal('4.5'),
                    'total_trips': 40,
                    'available': True
                }
            )

        # Create sample campervans
        campervan_city = CampervanCity.objects.first()
        force_brand = CampervanBrand.objects.filter(name__icontains='Force').first()
        diesel_fuel = CampervanFuelType.objects.filter(type='Diesel').first()
        campervan_manual = CampervanTransmission.objects.filter(type='Manual').first()
        campervan_year_2022 = CampervanModelYear.objects.filter(year=2022).first()
        portable_toilet = CampervanToilet.objects.filter(type__icontains='Portable').first()
        outdoor_shower = CampervanShower.objects.filter(type__icontains='Outdoor').first()

        if all([campervan_city, force_brand, diesel_fuel, campervan_manual, campervan_year_2022, portable_toilet, outdoor_shower]):
            campervan1, created = Campervan.objects.get_or_create(
                title='Force Traveller Adventure',
                defaults={
                    'model': 'Traveller 3350',
                    'description': 'Spacious campervan perfect for family adventures',
                    'city': campervan_city,
                    'brand': force_brand,
                    'fuel_type': diesel_fuel,
                    'transmission': campervan_manual,
                    'model_year': campervan_year_2022,
                    'toilet': portable_toilet,
                    'shower': outdoor_shower,
                    'service_provider': service_provider1,
                    'price_per_hour': Decimal('800.00'),
                    'price_per_day': Decimal('6000.00'),
                    'seating_capacity': 9,
                    'sleeping_capacity': 4,
                    'engine_capacity': '2596cc',
                    'baggage_capacity': 500,
                    'safety_deposit': Decimal('25000.00'),
                    'rating': Decimal('4.3'),
                    'total_trips': 15,
                    'available': True
                }
            )

        # Create sample hotels
        hotel_city = HotelCity.objects.first()
        hotel_property = PropertyType.objects.filter(type='Hotel').first()
        double_bed = BedPreference.objects.filter(type__icontains='Double').first()
        instant_book = ReservationType.objects.filter(type__icontains='Instant').first()

        if all([hotel_city, hotel_property, double_bed, instant_book]):
            hotel1, created = Hotel.objects.get_or_create(
                title='Nomad Paradise Hotel',
                defaults={
                    'description': 'Comfortable stay for digital nomads with all amenities',
                    'city': hotel_city,
                    'area': 'Business District',
                    'address': '123 Hotel Street, City Center',
                    'property_type': hotel_property,
                    'bed_preference': double_bed,
                    'reservation_type': instant_book,
                    'service_provider': service_provider2,
                    'bedrooms': 1,
                    'bathrooms': 1,
                    'guest_capacity': 2,
                    'price_per_day': Decimal('2500.00'),
                    'safety_deposit': Decimal('5000.00'),
                    'operating_hours': '24/7',
                    'documents_required': 'Valid ID proof',
                    'terms_and_conditions': 'Standard hotel terms apply',
                    'duration': '1week',
                    'rating': Decimal('4.6'),
                    'total_bookings': 35,
                    'available': True
                }
            )

        # Create sample guided trips
        trip_region = TripRegion.objects.first()
        trip_city = TripCity.objects.first()
        adventure_type = TripType.objects.filter(type='Adventure').first()
        moderate_level = TripDifficultyLevel.objects.filter(level__icontains='Moderate').first()
        group_join = JoinType.objects.filter(type='Group').first()

        if all([trip_region, trip_city, adventure_type, moderate_level, group_join]):
            trip1, created = GuidedTrip.objects.get_or_create(
                trip_name='Himalayan Adventure Ride',
                defaults={
                    'description': 'Epic motorcycle journey through the Himalayas',
                    'vehicle_type': '2_wheeler',
                    'trip_type': adventure_type,
                    'difficulty_level': moderate_level,
                    'region': trip_region,
                    'from_destination': trip_city,
                    'to_destination': trip_city,
                    'join_type': group_join,
                    'duration_days': 7,
                    'distance_km': Decimal('1200.50'),
                    'group_capacity': 15,
                    'min_participants': 5,
                    'fare_per_person': Decimal('25000.00'),
                    'created_by': service_provider1,
                    'guide_name': 'Rajesh Kumar',
                    'guide_contact': '+91-9876543220',
                    'start_date': date.today() + timedelta(days=30),
                    'end_date': date.today() + timedelta(days=37),
                    'registration_deadline': date.today() + timedelta(days=20),
                    'requirements': 'Valid driving license, riding experience',
                    'terms_and_conditions': 'Standard terms apply',
                    'rating': Decimal('4.7'),
                    'total_reviews': 12,
                    'total_trips_completed': 8
                }
            )

        # Create sample pilgrim destinations
        pilgrim_region = PilgrimRegion.objects.first()
        
        if pilgrim_region:
            destination1, created = PilgrimageDestination.objects.get_or_create(
                name='Vaishno Devi',
                defaults={
                    'city': 'Katra',
                    'state': 'Jammu & Kashmir',
                    'region': pilgrim_region,
                    'description': 'Holy shrine of Mata Vaishno Devi',
                    'significance': 'One of the most revered Hindu temples',
                    'best_time_to_visit': 'March to October',
                    'latitude': Decimal('32.9715'),
                    'longitude': Decimal('74.9513')
                }
            )

        # Create sample pilgrim tours
        pilgrim_package = PilgrimPackageType.objects.filter(type='Group').first()
        pilgrim_easy = PilgrimDifficultyLevel.objects.filter(level='Easy').first()

        if all([pilgrim_region, pilgrim_package, pilgrim_easy]):
            tour1, created = PilgrimTour.objects.get_or_create(
                title='Char Dham Yatra',
                defaults={
                    'description': 'Complete Char Dham pilgrimage tour',
                    'region': pilgrim_region,
                    'state': 'Uttarakhand',
                    'duration_days': 12,
                    'difficulty_level': pilgrim_easy,
                    'package_type': pilgrim_package,
                    'max_participants': 25,
                    'price_per_person': Decimal('35000.00'),
                    'service_provider': service_provider1,
                    'guide_included': True,
                    'guide_languages': ['Hindi', 'English'],
                    'start_date': date.today() + timedelta(days=45),
                    'end_date': date.today() + timedelta(days=57),
                    'requirements': 'Medical fitness certificate',
                    'terms_and_conditions': 'Standard pilgrimage tour terms apply',
                    'rating': Decimal('4.8'),
                    'total_reviews': 20,
                    'is_active': True
                }
            )

        # Create sample user stories
        story_city = StoryCity.objects.first()
        mountain_place = StoryPlaceType.objects.filter(type='Mountain').first()
        solo_journey = StoryJourneyType.objects.filter(type__icontains='Solo').first()

        if all([story_city, mountain_place, solo_journey]):
            story1, created = UserStory.objects.get_or_create(
                title='My Solo Trek to the Himalayas',
                defaults={
                    'content': 'An amazing journey of self-discovery in the mountains...',
                    'summary': 'Solo trekking adventure in the Himalayas',
                    'user': traveller1,
                    'place_type': mountain_place,
                    'journey_type': solo_journey,
                    'city': story_city,
                    'duration_days': 5,
                    'tags': ['adventure', 'solo', 'trekking', 'himalayas'],
                    'likes': 25,
                    'views': 150,
                    'is_approved': True,
                    'is_featured': True
                }
            )

        # Create sample travel insights
        tips_category = InsightCategory.objects.filter(name__icontains='Tips').first()

        if tips_category:
            insight1, created = TravelInsight.objects.get_or_create(
                title='Top 10 Budget Travel Tips for India',
                defaults={
                    'content': 'Comprehensive guide to traveling on a budget in India...',
                    'summary': 'Essential tips for budget travelers',
                    'insight_type': 'tip',
                    'category': tips_category,
                    'author': service_provider1,
                    'tags': ['budget', 'tips', 'india', 'travel'],
                    'relevant_states': ['Maharashtra', 'Delhi', 'Karnataka'],
                    'views': 500,
                    'likes': 45,
                    'shares': 12,
                    'is_published': True,
                    'is_featured': True
                }
            )

        # Create availability records for the next 30 days
        today = date.today()
        for i in range(30):
            current_date = today + timedelta(days=i)
            
            # Create bike availability
            if 'bike1' in locals():
                BikeAvailability.objects.get_or_create(
                    bike=bike1,
                    date=current_date,
                    defaults={'is_available': i % 7 != 0}  # Not available on every 7th day
                )

            # Create car availability  
            if 'car1' in locals():
                CarAvailability.objects.get_or_create(
                    car=car1,
                    date=current_date,
                    defaults={'is_available': i % 5 != 0}  # Not available on every 5th day
                )

            # Create campervan availability
            if 'campervan1' in locals():
                CampervanAvailability.objects.get_or_create(
                    campervan=campervan1,
                    date=current_date,
                    defaults={'is_available': i % 6 != 0}  # Not available on every 6th day
                )

            # Create hotel availability
            if 'hotel1' in locals():
                HotelAvailability.objects.get_or_create(
                    hotel=hotel1,
                    date=current_date,
                    defaults={'is_available': i % 8 != 0}  # Not available on every 8th day
                )

        # Create sample reviews
        if 'bike1' in locals():
            BikeReview.objects.get_or_create(
                bike=bike1,
                user=traveller1,
                defaults={
                    'rating': 4,
                    'review_text': 'Great bike for city rides. Fuel efficient and comfortable.',
                    'verified_booking': True
                }
            )

        if 'car1' in locals():
            CarReview.objects.get_or_create(
                car=car1,
                user=traveller2,
                defaults={
                    'rating': 5,
                    'review_text': 'Excellent car! Clean, well-maintained, and great service.',
                    'verified_booking': True
                }
            )

        if 'hotel1' in locals():
            HotelReview.objects.get_or_create(
                hotel=hotel1,
                user=traveller1,
                defaults={
                    'rating': 4,
                    'review_text': 'Perfect for digital nomads. Great WiFi and comfortable stay.',
                    'verified_booking': True
                }
            )

        # Create story interactions
        if 'story1' in locals():
            StoryLike.objects.get_or_create(
                story=story1,
                user=traveller2
            )
            
            StoryComment.objects.get_or_create(
                story=story1,
                user=traveller2,
                defaults={
                    'content': 'Amazing story! Inspired me to plan my own trek.'
                }
            )

        # Create insight interactions
        if 'insight1' in locals():
            InsightLike.objects.get_or_create(
                insight=insight1,
                user=traveller1
            )
            
            InsightComment.objects.get_or_create(
                insight=insight1,
                user=traveller2,
                defaults={
                    'content': 'Very helpful tips! Will definitely use these on my next trip.'
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded sample data!'))