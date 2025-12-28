from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

# Import all models for seeding
from apps.bikes.models import BikeCity, BikeTransmission, BikeFuelType, BikeBrand, BikeModelYear
from apps.cars.models import CarCity, CarTransmission, CarFuelType, CarType, CarBrand, CarModelYear
from apps.campervans.models import (
    CampervanCity, CampervanTransmission, CampervanFuelType, CampervanBrand, 
    CampervanModelYear, CampervanToilet, CampervanShower, CampervanAmenity
)
from apps.hotels.models import (
    HotelCity, PropertyType, BedPreference, HotelFacility, RoomFacility, 
    OutdoorFeature, ReservationType
)
from apps.guided_trips.models import (
    TripRegion, TripCity, TripType, TripDifficultyLevel, SupportFeature, JoinType
)
from apps.pilgrim.models import (
    PilgrimRegion, PilgrimPackageType, PilgrimFeature, PilgrimDifficultyLevel
)
from apps.stories.models import StoryPlaceType, StoryJourneyType, StoryCity
from apps.insights.models import InsightCategory

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed all lookup data for the TravellerClicks platform'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting comprehensive data seeding...'))

        # Create cities data
        cities_data = [
            'Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad',
            'Pune', 'Ahmedabad', 'Surat', 'Jaipur', 'Lucknow', 'Kanpur',
            'Nagpur', 'Indore', 'Thane', 'Bhopal', 'Visakhapatnam', 'Pimpri-Chinchwad',
            'Patna', 'Vadodara', 'Ghaziabad', 'Ludhiana', 'Agra', 'Nashik',
            'Faridabad', 'Meerut', 'Rajkot', 'Kalyan-Dombivali', 'Vasai-Virar', 'Varanasi',
            'Goa', 'Shimla', 'Manali', 'Dharamshala', 'Rishikesh', 'Haridwar',
            'Udaipur', 'Jodhpur', 'Pushkar', 'Mount Abu', 'Kochi', 'Alleppey',
            'Munnar', 'Thekkady', 'Mysore', 'Hampi', 'Coorg', 'Ooty',
            'Kodaikanal', 'Darjeeling', 'Gangtok', 'Shillong', 'Kaziranga'
        ]

        # Seed Trip Regions first (needed for TripCity)
        trip_regions = [
            ('North India', 'Northern states including Delhi, Punjab, Haryana, UP, HP, UK, J&K'),
            ('South India', 'Southern states including Tamil Nadu, Karnataka, Kerala, Andhra Pradesh, Telangana'),
            ('East India', 'Eastern states including West Bengal, Odisha, Jharkhand, Bihar'),
            ('West India', 'Western states including Maharashtra, Gujarat, Rajasthan, Goa'),
            ('Northeast India', 'Seven sister states of Northeast'),
            ('Central India', 'Central states including MP, Chhattisgarh')
        ]
        for name, desc in trip_regions:
            TripRegion.objects.get_or_create(name=name, defaults={'description': desc})

        # Seed Bike Cities
        for city_name in cities_data:
            BikeCity.objects.get_or_create(
                name=city_name,
                defaults={'state': 'India', 'country': 'India'}
            )

        # Seed Car Cities
        for city_name in cities_data:
            CarCity.objects.get_or_create(
                name=city_name,
                defaults={'state': 'India', 'country': 'India'}
            )

        # Seed Campervan Cities
        for city_name in cities_data:
            CampervanCity.objects.get_or_create(
                name=city_name,
                defaults={'state': 'India', 'country': 'India'}
            )

        # Seed Hotel Cities
        for city_name in cities_data:
            HotelCity.objects.get_or_create(
                name=city_name,
                defaults={'state': 'India', 'country': 'India'}
            )

        # Seed Trip Cities (with region reference)
        first_region = TripRegion.objects.first()
        for city_name in cities_data:
            TripCity.objects.get_or_create(
                name=city_name,
                defaults={'state': 'India', 'country': 'India', 'region': first_region}
            )

        # Seed Story Cities
        for city_name in cities_data:
            StoryCity.objects.get_or_create(
                name=city_name,
                defaults={'state': 'India', 'country': 'India'}
            )

        # Seed Bike Transmissions
        bike_transmissions = ['Manual', 'Automatic', 'Semi-Automatic', 'CVT']
        for transmission in bike_transmissions:
            BikeTransmission.objects.get_or_create(type=transmission)

        # Seed Car Transmissions
        car_transmissions = ['Manual', 'Automatic', 'CVT', 'AMT', 'DCT']
        for transmission in car_transmissions:
            CarTransmission.objects.get_or_create(type=transmission)

        # Seed Campervan Transmissions
        for transmission in car_transmissions:
            CampervanTransmission.objects.get_or_create(type=transmission)

        # Seed Fuel Types
        fuel_types = ['Petrol', 'Diesel', 'Electric', 'Hybrid', 'CNG', 'LPG']
        
        for fuel_type in fuel_types:
            if fuel_type in ['Petrol', 'Electric', 'Hybrid', 'CNG']:
                BikeFuelType.objects.get_or_create(type=fuel_type)
            CarFuelType.objects.get_or_create(type=fuel_type)
            CampervanFuelType.objects.get_or_create(type=fuel_type)

        # Seed Bike Brands
        bike_brands = [
            'Hero MotoCorp', 'Honda', 'Bajaj', 'TVS', 'Yamaha', 'Royal Enfield',
            'Suzuki', 'KTM', 'Kawasaki', 'Harley-Davidson', 'BMW', 'Ducati',
            'Triumph', 'Mahindra', 'Benelli', 'Aprilia', 'Piaggio', 'Ather',
            'Ola Electric', 'Revolt', 'Okinawa', 'Ampere', 'Hero Electric'
        ]
        for brand in bike_brands:
            BikeBrand.objects.get_or_create(name=brand)

        # Seed Car Brands
        car_brands = [
            'Maruti Suzuki', 'Hyundai', 'Tata', 'Mahindra', 'Toyota', 'Honda',
            'Ford', 'Chevrolet', 'Nissan', 'Volkswagen', 'Skoda', 'Renault',
            'Kia', 'MG Motor', 'Jeep', 'BMW', 'Mercedes-Benz', 'Audi'
        ]
        for brand in car_brands:
            CarBrand.objects.get_or_create(name=brand)

        # Seed Campervan Brands
        campervan_brands = [
            'Force Motors', 'Tata Motors', 'Mahindra', 'Ashok Leyland',
            'Eicher Motors', 'SML Isuzu', 'Bharat Benz', 'Volvo', 'Scania'
        ]
        for brand in campervan_brands:
            CampervanBrand.objects.get_or_create(name=brand)

        # Seed Car Types
        car_types = ['Hatchback', 'Sedan', 'SUV', 'Crossover', 'MPV', 'Convertible', 'Coupe', 'Wagon', 'Pickup', 'Luxury']
        for car_type in car_types:
            CarType.objects.get_or_create(type=car_type)

        # Seed Model Years
        current_year = 2024
        for year in range(2010, current_year + 2):
            BikeModelYear.objects.get_or_create(year=year)
            CarModelYear.objects.get_or_create(year=year)
            CampervanModelYear.objects.get_or_create(year=year)

        # Seed Campervan specific data
        toilet_types = [
            'Portable Toilet',
            'Cassette Toilet',
            'Composting Toilet',
            'No Toilet'
        ]
        for name in toilet_types:
            CampervanToilet.objects.get_or_create(type=name)

        shower_types = [
            'Indoor Shower',
            'Outdoor Shower',
            'Portable Shower',
            'No Shower'
        ]
        for name in shower_types:
            CampervanShower.objects.get_or_create(type=name)

        amenities = [
            'Air Conditioning', 'Kitchen', 'Refrigerator', 'WiFi', 'GPS Navigation',
            'Solar Panel', 'Generator', 'Water Tank', 'Waste Water Tank',
            'Bed Linen', 'Towels', 'Cookware', 'Outdoor Furniture', 'Bike Rack',
            'Awning', 'TV/Entertainment', 'Heating', 'Hot Water', 'Inverter'
        ]
        for amenity in amenities:
            CampervanAmenity.objects.get_or_create(name=amenity)

        # Seed Hotel data
        property_types = [
            'Hotel', 'Guest House', 'Hostel', 'Resort', 'Apartment',
            'Villa', 'Cottage', 'Homestay', 'Lodge', 'Treehouse'
        ]
        for prop_type in property_types:
            PropertyType.objects.get_or_create(type=prop_type)

        bed_preferences = [
            'Single Bed', 'Double Bed', 'Queen Bed', 'King Bed',
            'Bunk Bed', 'Sofa Bed', 'Twin Beds'
        ]
        for bed_pref in bed_preferences:
            BedPreference.objects.get_or_create(type=bed_pref)

        hotel_facilities = [
            'Free WiFi', 'Swimming Pool', 'Gym/Fitness Center', 'Spa',
            'Restaurant', 'Bar', 'Room Service', 'Laundry Service',
            'Airport Shuttle', 'Parking', 'Pet Friendly', 'Business Center',
            'Conference Rooms', 'Concierge', '24/7 Front Desk'
        ]
        for facility in hotel_facilities:
            HotelFacility.objects.get_or_create(name=facility)

        room_facilities = [
            'Air Conditioning', 'Private Bathroom', 'TV', 'Mini Bar',
            'Tea/Coffee Maker', 'Safe', 'Balcony', 'Kitchen',
            'Refrigerator', 'Microwave', 'Washing Machine', 'Iron',
            'Hair Dryer', 'Bathtub', 'Shower'
        ]
        for facility in room_facilities:
            RoomFacility.objects.get_or_create(name=facility)

        outdoor_features = [
            'Garden', 'Terrace', 'Beach Access', 'Mountain View',
            'Lake View', 'Forest View', 'City View', 'Playground',
            'BBQ Area', 'Outdoor Seating', 'Hiking Trails', 'Water Sports'
        ]
        for feature in outdoor_features:
            OutdoorFeature.objects.get_or_create(feature=feature)

        reservation_types = [
            'Instant Book', 'Request to Book', 'Call to Book'
        ]
        for res_type in reservation_types:
            ReservationType.objects.get_or_create(type=res_type)

        # Seed Trip data
        trip_types = [
            'Adventure', 'Leisure', 'Cultural', 'Spiritual', 'Wildlife',
            'Photography', 'Food & Culinary', 'Historical', 'Beach', 'Mountain'
        ]
        for trip_type in trip_types:
            TripType.objects.get_or_create(type=trip_type)

        difficulty_levels = [
            ('Easy', 'Suitable for beginners'),
            ('Moderate', 'Some experience required'),
            ('Challenging', 'Advanced level'),
            ('Expert', 'Professional level')
        ]
        for level, desc in difficulty_levels:
            TripDifficultyLevel.objects.get_or_create(level=level, defaults={'description': desc})

        support_features = [
            'Fuel Support', 'Mechanical Support', 'Medical Support',
            'Luggage Transport', 'Photography Service', 'Local Guide',
            'Meal Arrangements', 'Accommodation Booking', 'Route Planning',
            'Emergency Assistance'
        ]
        for feature in support_features:
            SupportFeature.objects.get_or_create(feature=feature)

        join_types = [
            'Individual', 'Group', 'Couple', 'Family', 'Corporate'
        ]
        for join_type in join_types:
            JoinType.objects.get_or_create(type=join_type)

        # Seed Pilgrim data
        pilgrim_regions = [
            'North India', 'South India', 'East India', 'West India',
            'Northeast India', 'Central India', 'Char Dham', 'Panch Kedar'
        ]
        for region in pilgrim_regions:
            PilgrimRegion.objects.get_or_create(name=region)

        package_types = [
            'Individual', 'Group', 'VIP', 'Budget', 'Luxury',
            'Family', 'Senior Citizen', 'Student'
        ]
        for package in package_types:
            PilgrimPackageType.objects.get_or_create(type=package)

        pilgrim_features = [
            'Guided Tours', 'Transportation', 'Meals Included',
            'Accommodation', 'Darshan Arrangement', 'Puja Services',
            'Local Guide', 'Cultural Programs', 'Medical Assistance',
            'Photography', 'Shopping Tours', 'Religious Ceremonies'
        ]
        for feature in pilgrim_features:
            PilgrimFeature.objects.get_or_create(feature=feature)

        pilgrim_difficulty = [
            'Easy', 'Moderate', 'Challenging', 'Strenuous'
        ]
        for level in pilgrim_difficulty:
            PilgrimDifficultyLevel.objects.get_or_create(level=level)

        # Seed Story data
        place_types = [
            'City', 'Beach', 'Mountain', 'Forest', 'Desert', 'Lake',
            'River', 'Temple', 'Fort', 'Palace', 'Market', 'Village'
        ]
        for place_type in place_types:
            StoryPlaceType.objects.get_or_create(type=place_type)

        journey_types = [
            'Solo Travel', 'Group Travel', 'Family Trip', 'Couple Trip',
            'Adventure Trip', 'Cultural Journey', 'Spiritual Journey',
            'Food Journey', 'Photography Expedition', 'Business Travel'
        ]
        for journey_type in journey_types:
            StoryJourneyType.objects.get_or_create(type=journey_type)

        # Seed Insights data
        insight_categories = [
            ('Travel Tips', 'Travel Tips related content'),
            ('Destination Guides', 'Destination Guides related content'),
            ('Budget Travel', 'Budget Travel related content'),
            ('Luxury Travel', 'Luxury Travel related content'),
            ('Adventure Travel', 'Adventure Travel related content'),
            ('Cultural Insights', 'Cultural Insights related content'),
            ('Food & Travel', 'Food & Travel related content'),
            ('Travel Photography', 'Travel Photography related content'),
            ('Safety Tips', 'Safety Tips related content'),
            ('Packing Guides', 'Packing Guides related content')
        ]
        for name, desc in insight_categories:
            InsightCategory.objects.get_or_create(
                name=name,
                defaults={'description': desc, 'icon': f'{name.lower().replace(" ", "_")}_icon'}
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded all lookup data!'))